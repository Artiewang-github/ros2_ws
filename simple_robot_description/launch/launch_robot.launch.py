import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    package_name = 'simple_robot_description'
    
    # Safely look up package paths
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    urdf_path = os.path.join(pkg_share, 'urdf', 'simple_robot.urdf.xacro')
    #urdf_path = os.path.join(pkg_share, 'urdf', 'simple_robot.urdf')
    controller_config_path = os.path.join(pkg_share, 'config', 'controllers.yaml')
    rviz_config_path = os.path.join(pkg_share, 'config', 'simple_robot.rviz')

    # Read URDF content
    with open(urdf_path, 'r') as f:
        robot_description_content = f.read()

    # Nodes 
    # 1. Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}]
    )

    # 2. Controller Manager
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[{'robot_description': robot_description_content}, controller_config_path],
        output='screen'
    )

    # 3. Spawner for Joint State Broadcaster
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
    )

    # 4. Spawner for Position Controller
    position_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['position_controller', '--controller-manager', '/controller_manager'],
    )

    # Optional: Automatically launch RViz2 alongside everything else!
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]
    )

    return LaunchDescription([
        robot_state_publisher,
        controller_manager,
        joint_state_broadcaster_spawner,
        position_controller_spawner,
        rviz
    ])
