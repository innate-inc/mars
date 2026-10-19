# MARS robot descriptions

Two self-contained ROS description variants, vendored from Innate OS:

| File | Base mechanics | Purpose |
|---|---|---|
| `urdf/mars.urdf` | Wheels are fixed collision shapes; no rotating wheel/caster joints | Reference model from Innate OS main at `4953aaa37f` (1.365 kg declared mass) |
| `urdf/mars_physics.urdf` | Articulated drive wheels and passive caster | Experimental free-base dynamics (2.99831 kg including a provisional 0.50 kg battery) |

Both include the current reference arm joint limits, sensor frames and detailed
gripper colliders. “Fixed-wheel” does not mean wheel geometry is absent.
The physics model is **not hardware calibrated**. Read [PHYSICS.md](PHYSICS.md)
for provenance, assumptions, simulation results and remaining validation.

## Load

This directory is an `ament_cmake` package named `mars_description`. Place it in
a ROS 2 workspace's `src/`, build with `colcon build --packages-select
mars_description`, and source the workspace's `install/setup.bash`.
Select the desired file explicitly when configuring robot_state_publisher or
an importer; this package does not change any production launch configuration.
Do not install this package alongside another package with the same name in
the same workspace.

All meshes are bundled. Mesh URIs use `package://mars_description/`; outside
ROS, map that prefix to this directory's absolute path in your importer.
The MuJoCo test harness demonstrates this resolution and adds simulator-specific
actuators, floor contact, free base and the gripper mimic constraint. Those are
not automatically configured by loading a URDF alone.

## Test

From the repository root:

```sh
uv run --python 3.11 --with mujoco==3.10.0 --with numpy==2.2.6 python models/mars_description/test/test_physics.py
```

No ROS, external assets, or Innate OS checkout is required for these tests.
The reference URDF is pinned; preservation checks compare the experimental file
against that snapshot, not against live upstream main.

## Provenance and license

Reference: https://github.com/innate-inc/innate-os/tree/4953aaa37f4633511b8308c201a2ab9c961347f9

Historical physics components: https://github.com/innate-inc/innate-os/tree/6f8abd5b942a7260978b0be99aae36b7408cfbd1

This imported package retains its upstream Apache-2.0 license; see [LICENSE](LICENSE).
The experimental physics variant and test harness were added October 18, 2026.
