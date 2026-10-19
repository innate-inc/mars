"""Run with sim's Python environment: python test/test_physics.py.

Imports the shipped URDF into MuJoCo with a free base, frictional ground,
wheel motor torques and passive caster. No forces are applied to the base.
"""

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import mujoco
import numpy as np

PACKAGE = Path(__file__).resolve().parents[1]
URDF = PACKAGE / "urdf/mars_physics.urdf"
# MuJoCo-only contact settings from innate-os world.py at 4953aaa37f.
# Kept local so this package can be tested without an innate-os checkout.
FINGER_LINKS = ("link61", "link62")
FINGER_CONDIM = 6
FINGER_FRICTION = (2.0, 0.05, 0.02)
FINGER_SOLREF = (0.005, 1.0)
FINGER_SOLIMP = (0.95, 0.99, 0.001, 0.5, 2)
FINGER_DAMPING = 1.0
FINGER_ARMATURE = 1e-4


def build_model(battery_mass=0.5, ball=False):
    text = URDF.read_text().replace("package://mars_description/", str(PACKAGE) + "/")
    text = text.replace(
        '<robot name="mars_bot">',
        '<robot name="mars_bot"><mujoco><compiler discardvisual="false" fusestatic="false"/></mujoco>',
    )
    spec = mujoco.MjSpec.from_string(text)
    battery = spec.body("battery")
    battery.inertia *= battery_mass / battery.mass
    battery.mass = battery_mass
    spec.worldbody.add_light(pos=[1, -1, 2], dir=[-1, 1, -2], diffuse=[0.8, 0.8, 0.8])
    spec.worldbody.add_light(pos=[-1, 1, 2], dir=[1, -1, -2], diffuse=[0.6, 0.6, 0.6])
    spec.option.timestep = 0.001
    spec.option.integrator = mujoco.mjtIntegrator.mjINT_IMPLICITFAST
    base = spec.body("base_link")
    base.add_freejoint(name="base_free")
    base.pos = [0, 0, 0.005]
    spec.worldbody.add_geom(
        name="floor",
        type=mujoco.mjtGeom.mjGEOM_PLANE,
        size=[5, 5, 0.1],
        friction=[0.8, 0.001, 0.0001],
    )
    spec.add_exclude(bodyname1="link61", bodyname2="link62")
    for name in FINGER_LINKS:
        for g in spec.body(name).geoms:
            if g.contype:
                g.condim = FINGER_CONDIM
                g.priority = 2
                g.friction = FINGER_FRICTION
                g.solref = FINGER_SOLREF
                g.solimp = FINGER_SOLIMP
    for name in ["joint6", "joint6M"]:
        spec.joint(name).damping = [FINGER_DAMPING, 0, 0]
        spec.joint(name).armature = FINGER_ARMATURE
    if ball:
        b = spec.worldbody.add_body(name="test_ball", pos=[0, 0, 1])
        b.add_freejoint(name="ball_free")
        b.add_geom(
            name="ball",
            type=mujoco.mjtGeom.mjGEOM_SPHERE,
            size=[0.01, 0, 0],
            mass=0.01,
            rgba=[1, 0.2, 0.1, 1],
        )
    mimic = spec.add_equality(
        name="gripper_mimic",
        type=mujoco.mjtEq.mjEQ_JOINT,
        name1="joint6M",
        name2="joint6",
    )
    mimic.data[:5] = [0, -1, 0, 0, 0]
    for name in ["left_wheel_joint", "right_wheel_joint"]:
        a = spec.add_actuator(name=name, target=name, trntype=mujoco.mjtTrn.mjTRN_JOINT)
        a.set_to_velocity(kv=0.05)
        a.forcelimited = True
        a.forcerange = [-0.25, 0.25]
        a.ctrllimited = True
        a.ctrlrange = [-10.3, 10.3]
    for j in ET.parse(URDF).getroot().findall("joint"):
        if j.get("type") != "revolute" or j.get("name") == "joint6M":
            continue
        a = spec.add_actuator(
            name=j.get("name"), target=j.get("name"), trntype=mujoco.mjtTrn.mjTRN_JOINT
        )
        a.set_to_position(kp=20, kv=1)
        a.forcelimited = True
        a.forcerange = [-2, 2]
    return spec.compile()


def simulate(left=0.0, right=0.0, duration=4.0, caster=0.0, battery_mass=0.5):
    model = build_model(battery_mass=battery_mass)
    data = mujoco.MjData(model)
    data.qpos[model.joint("caster_frame_joint").qposadr[0]] = caster
    pose = {
        "joint1": 1.445,
        "joint2": -1.20,
        "joint3": 1.50,
        "joint4": 0.446,
        "joint5": -0.089,
    }
    for name, value in pose.items():
        data.qpos[model.joint(name).qposadr[0]] = value
        data.ctrl[model.actuator(name).id] = value
    for _ in range(1500):
        mujoco.mj_step(model, data)
    start = data.xpos[model.body("base_link").id].copy()
    data.ctrl[model.actuator("left_wheel_joint").id] = left
    data.ctrl[model.actuator("right_wheel_joint").id] = right
    for _ in range(round(duration / model.opt.timestep)):
        mujoco.mj_step(model, data)
    assert np.isfinite(data.qpos).all()
    assert not any(w.number for w in data.warning)
    delta = data.xpos[model.body("base_link").id] - start
    rot = data.xmat[model.body("base_link").id].reshape(3, 3)
    return model, data, delta, rot


class PhysicsModelTest(unittest.TestCase):
    def test_structure_and_preserved_kinematics(self):
        current = ET.parse(PACKAGE / "urdf/mars.urdf").getroot()
        physics = ET.parse(URDF).getroot()

        def signature(el):
            return el.tag, el.attrib, [signature(c) for c in el]

        for j in current.findall("joint"):
            self.assertEqual(
                signature(j), signature(physics.find(f"joint[@name='{j.get('name')}']"))
            )
        for link in current.findall("link"):
            if link.get("name") == "base_link":
                continue
            other = physics.find(f"link[@name='{link.get('name')}']")
            for tag in ["visual", "collision"]:
                self.assertEqual(
                    [signature(c) for c in link.findall(tag)],
                    [signature(c) for c in other.findall(tag)],
                )
        names = [link.get("name") for link in physics.findall("link")]
        self.assertEqual(len(names), len(set(names)))
        children = [j.find("child").get("link") for j in physics.findall("joint")]
        self.assertEqual(set(names) - set(children), {"base_link"})
        self.assertEqual(len(children), len(set(children)))
        for mesh in physics.findall(".//mesh"):
            self.assertTrue(
                Path(
                    mesh.get("filename").replace(
                        "package://mars_description/", str(PACKAGE) + "/"
                    )
                ).is_file()
            )
        for link in physics.findall("link"):
            inertial = link.find("inertial")
            if inertial is None:
                continue
            self.assertGreater(float(inertial.find("mass").get("value")), 0)
            i = {k: float(v) for k, v in inertial.find("inertia").attrib.items()}
            eig = np.linalg.eigvalsh(
                [
                    [i["ixx"], i["ixy"], i["ixz"]],
                    [i["ixy"], i["iyy"], i["iyz"]],
                    [i["ixz"], i["iyz"], i["izz"]],
                ]
            )
            self.assertGreater(eig[0], 0)
            self.assertLessEqual(eig[2], eig[0] + eig[1] + 1e-9)

    def test_drive(self):
        for speed in [4.0, -4.0]:
            with self.subTest(speed=speed):
                _m, _d, delta, r = simulate(speed, speed)
                print("drive", speed, "delta", delta, "upright", r[2, 2])
                self.assertGreater(delta[0] * np.sign(speed), 0.25)
                self.assertLess(abs(delta[1]), 0.15)
                self.assertGreater(r[2, 2], 0.97)
                self.assertLess(abs(delta[2]), 0.02)

    def test_stop(self):
        m, d, _delta, _r = simulate(4, 4)
        d.ctrl[m.actuator("left_wheel_joint").id] = 0
        d.ctrl[m.actuator("right_wheel_joint").id] = 0
        start = d.xpos[m.body("base_link").id].copy()
        for _ in range(1000):
            mujoco.mj_step(m, d)
        self.assertLess(np.linalg.norm(d.xpos[m.body("base_link").id] - start), 0.04)
        self.assertLess(
            np.linalg.norm(d.qvel[m.joint("base_free").dofadr[0] :][:6]), 0.01
        )

    def test_rest_and_turn(self):
        for speeds in [(0, 0), (-3, 3), (3, -3)]:
            with self.subTest(speeds=speeds):
                _m, _d, delta, r = simulate(*speeds)
                yaw = np.arctan2(r[1, 0], r[0, 0])
                print("turn", speeds, "delta", delta, "yaw", yaw, "upright", r[2, 2])
                self.assertGreater(r[2, 2], 0.97)
                if speeds == (0, 0):
                    self.assertLess(np.linalg.norm(delta), 0.02)
                else:
                    self.assertGreater(yaw * np.sign(speeds[1]), 0.3)

    def test_gripper_holds_after_fixture_release(self):
        m = build_model(ball=True)
        d = mujoco.MjData(m)
        pose = {
            "joint1": 1.445,
            "joint2": -1.2,
            "joint3": 1.5,
            "joint4": 0.446,
            "joint5": -0.089,
            "joint6": 0.6,
        }
        for n, v in pose.items():
            d.qpos[m.joint(n).qposadr[0]] = v
            d.ctrl[m.actuator(n).id] = v
        d.qpos[m.joint("joint6M").qposadr[0]] = -0.6
        for _ in range(1500):
            mujoco.mj_step(m, d)
        bq = m.joint("ball_free").qposadr[0]
        bv = m.joint("ball_free").dofadr[0]
        w = m.body("link5").id
        # Placement fixture holds a 10 g, 20 mm sphere while the jaws close.
        # All fixture forcing stops before either retention assertion.
        for _ in range(1500):
            d.ctrl[m.actuator("joint6").id] = 0
            d.qpos[bq : bq + 3] = d.xpos[w] + d.xmat[w].reshape(3, 3) @ np.array(
                [0.086, 0, 0.01945]
            )
            d.qvel[bv : bv + 6] = 0
            mujoco.mj_step(m, d)
        for _ in range(1500):
            mujoco.mj_step(m, d)
        relative = d.xmat[w].reshape(3, 3).T @ (
            d.xpos[m.body("test_ball").id] - d.xpos[w]
        )
        d.ctrl[m.actuator("joint1").id] = 1.1
        for _ in range(2000):
            mujoco.mj_step(m, d)
        drift = np.linalg.norm(
            d.xmat[w].reshape(3, 3).T @ (d.xpos[m.body("test_ball").id] - d.xpos[w])
            - relative
        )
        self.assertLess(drift, 0.005)
        self.assertGreater(d.xpos[m.body("test_ball").id][2], 0.04)
        fingers = set()
        for c in d.contact:
            bodies = {
                m.body(m.geom_bodyid[c.geom1]).name,
                m.body(m.geom_bodyid[c.geom2]).name,
            }
            if "test_ball" in bodies:
                fingers.update(bodies - {"test_ball"})
        self.assertEqual(fingers, {"link61", "link62"})
        self.assertFalse(any(warning.number for warning in d.warning))

    def test_battery_sensitivity_and_support(self):
        for mass in [0.35, 0.50, 0.65]:
            with self.subTest(mass=mass):
                m, d, delta, r = simulate(4, 4, battery_mass=mass)
                self.assertGreater(r[2, 2], 0.999)
                self.assertGreater(delta[0], 0.5)
                self.assertLess(abs(delta[1]), 0.03)
                floor_bodies = {
                    m.body(m.geom_bodyid[c.geom2]).name
                    for c in d.contact
                    if m.geom(c.geom1).name == "floor"
                }
                self.assertEqual(
                    floor_bodies, {"left_wheel", "right_wheel", "caster_wheel"}
                )

    def test_caster_realigns(self):
        m, d, delta, _r = simulate(4, 4, caster=np.pi / 2)
        angle = d.qpos[m.joint("caster_frame_joint").qposadr[0]]
        print("caster", angle, "delta", delta)
        self.assertLess(abs(np.arctan2(np.sin(angle), np.cos(angle))), 0.4)
        self.assertGreater(delta[0], 0.25)


if __name__ == "__main__":
    unittest.main()
