# Experimental articulated MARS model

`urdf/mars_physics.urdf` is an opt-in model. `mars.urdf`, the production
launch paths, and the existing planar simulator are unchanged. The package's
CMake directory install includes the new URDF and meshes.

## Sources and compatibility

- Current arm kinematics, joint limits, frames, arm/head visuals and collision
  shapes: `innate-os` commit `4953aaa37f4633511b8308c201a2ab9c961347f9`.
- Separate wheel/caster/base meshes, wheel joints, component inertias and motor
  masses: historical physics commit `6f8abd5b942a7260978b0be99aae36b7408cfbd1`.
- The older base mesh excludes the wheels (unlike the current combined mesh),
  avoiding duplicate static wheels. Motor links m2–m6 carry inertia only: the
  reference arm visuals/colliders already represent their external envelopes.
- All current joints retain their names, origins, axes, limits and mimic rules.
  New joints: left_wheel_joint, right_wheel_joint, caster_frame_joint,
  caster_wheel_joint, m2_joint–m6_joint, and battery_joint.
- Source meshes retain the upstream Apache-2.0 license (included in this package). No mesh was scaled.

The existing simulator applies forces to a planar base and deliberately removes
wheel friction. Do not point that loader at this model and expect wheel dynamics.
Use the free-base harness in `test/test_physics.py` as an integration example;
it applies velocity-servo torque only to the wheels. A production ROS/controller
integration is not included. Publish the additional wheel/caster joint states
when using this file with robot_state_publisher. MuJoCo does not import URDF mimic
constraints: the harness explicitly adds the gripper equality constraint.

## Changes requiring hardware calibration

These are engineering assumptions, not measured hardware parameters:

- Mass inventory is inherited from the historical branch. The model totals
  **2.99831 kg**, including an explicit **0.50 kg provisional battery** centered
  on the current rear-tray collider at (-0.1895, 0, 0.0466) m. Battery inertia is
  calculated from a uniform 70 × 140 × 40 mm box. No new battery collider/visual
  is added because the rear-tray envelope covers it. The historical base mass
  comment lists plastic/lidar/Jetson/USB hub and does not account for a battery.
  Reconcile that inventory before trusting total mass; it is not a weigh-in.
- Without the battery estimate the inherited inventory tips onto the arm mount,
  unloading the caster, even in the folded test pose. This is why the missing
  inventory is explicit rather than silently moving the base COM.
- Drive wheel dimensions/locations retain the old values (37.25 mm radius,
  176.4 mm track, 20 mm collision width). The corresponding STL extents are
  approximately 37.22 mm radius. Historical damping of 0.1 N m s/rad would
  consume the 0.25 N m torque limit at just 2.5 rad/s; the experimental damping
  is 0.001, with zero Coulomb joint friction, pending drivetrain measurements.
- The caster collider is a 13 mm radius, 28 mm wide cylinder aligned with its
  axle, matching the STL envelope, rather than a sphere. The axle height is
  adjusted to 13 mm to touch the same ground plane as the drive wheels. Caster
  damping is 0.00001 with zero joint friction; these values are uncalibrated.
- The chassis box's underside is raised from 0 to 30 mm to clear the caster
  sweep. Its top and horizontal envelope are retained. The lower chassis
  interior is omitted rather than represented by a solid box through the
  caster. This is unsuitable for validating low-obstacle/underbody impacts
  until a measured underbody decomposition replaces it. Other base protrusion
  colliders, and all arm/gripper/head colliders, are retained.
- Surface friction belongs to the simulator, not core URDF. The harness uses
  0.8 floor sliding friction and the existing simulator's finger contact
  settings. Neither proves real tire slip or real grasp force accuracy.

Measure battery mass/placement, whole-robot COM, drivetrain drag/torque and
caster contact geometry before using this model for sim-to-real conclusions.
Do not make it the production default on the strength of these smoke tests.

## Verification

From this repository root (Python 3.11 and uv):

```sh
uv run --python 3.11 --with mujoco==3.10.0 --with numpy==2.2.6 python models/mars_description/test/test_physics.py
```

Seven unittest cases exercise the shipped URDF with MuJoCo, gravity, a free base,
frictional ground, passive caster and torque-limited wheel servos:

- current joint definitions and non-base visuals/collisions preserved;
  all mesh paths resolve; masses/inertias are positive and physically admissible;
- settling, forward/reverse driving, stopping and turns in both directions;
- ground support only on left/right wheels and caster, across 0.35/0.50/0.65 kg
  battery assumptions;
- caster initially sideways swivels toward trailing alignment while driving;
- a 10 g sphere remains between both fingers after its placement fixture is
  released, including a subsequent arm movement (retention test, not an
  autonomous pickup).

Validated with MuJoCo 3.10.0. At 4 rad/s on both wheels the model travels about
0.576 m in four seconds, with under 6 mm lateral drift in the aligned-caster
cases. A sideways caster causes substantial transient veering (~0.31 m lateral
in the four-second test); this is not a navigation accuracy claim.

No physical robot run, ROS launch, rough terrain, slopes, broad arm workspace,
controller policy training, or autonomous pickup was validated. Keep this model
experimental until those relevant to its intended use are tested. Future
updates to the vendored mars.urdf reference should be reconciled into this file; the preservation test
intentionally fails when joint/collision definitions diverge.
