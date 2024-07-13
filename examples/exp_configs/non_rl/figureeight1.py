"""Benchmark for figureeight1.

Trains a fraction of vehicles in a ring road structure to regulate the flow of
vehicles through an intersection. In this example, every other vehicle in the
network is an autonomous vehicle.

- **Action Dimension**: (7, )
- **Observation Dimension**: (28, )
- **Horizon**: 1500 steps
"""
from flow.envs import AccelEnv
from flow.networks import FigureEightNetwork
from copy import deepcopy
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams, \
    SumoCarFollowingParams
from flow.core.params import VehicleParams
from flow.controllers import IDMController, ContinuousRouter, RLController
from flow.controllers import LLMController
from flow.networks.figure_eight import ADDITIONAL_NET_PARAMS

# time horizon of a single rollout
HORIZON = 1500

# We place 8 autonomous vehicle and 8 human-driven vehicles in the network
vehicles = VehicleParams()
for i in range(7):
    vehicles.add(
        veh_id="human{}".format(i),
        acceleration_controller=(IDMController, {
            "noise": 0.2
        }),
        routing_controller=(ContinuousRouter, {}),
        car_following_params=SumoCarFollowingParams(
            speed_mode="obey_safe_speed",
            decel=1.5,
        ),
        num_vehicles=1)
    vehicles.add(
        veh_id="llm{}".format(i),
        acceleration_controller=(LLMController, {}),
        routing_controller=(ContinuousRouter, {}),
        car_following_params=SumoCarFollowingParams(
            speed_mode="obey_safe_speed",
        ),
        num_vehicles=1)

flow_params = dict(
    # name of the experiment
    exp_tag="figure_eight_1",

    # name of the flow environment the experiment is running on
    env_name=AccelEnv,

    # name of the network class the experiment is running on
    network=FigureEightNetwork,

    # simulator that is used by the experiment
    simulator='traci',

    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=SumoParams(
        sim_step=0.1,
        render=False,
    ),

    # environment related parameters (see flow.core.params.EnvParams)
    env=EnvParams(
        horizon=HORIZON,
        additional_params={
            "target_velocity": 20,
            "max_accel": 3,
            "max_decel": 3,
            "sort_vehicles": False
        },
    ),

    # network-related parameters (see flow.core.params.NetParams and the
    # network's documentation or ADDITIONAL_NET_PARAMS component)
    net=NetParams(
        additional_params=deepcopy(ADDITIONAL_NET_PARAMS),
    ),

    # vehicles to be placed in the network at the start of a rollout (see
    # flow.core.params.VehicleParams)
    veh=vehicles,

    # parameters specifying the positioning of vehicles upon initialization/
    # reset (see flow.core.params.InitialConfig)
    initial=InitialConfig(),
)