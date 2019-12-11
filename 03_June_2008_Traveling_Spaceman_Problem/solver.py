"""Simple travelling salesman problem between cities."""

# python -m pip install --upgrade --user ortools
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['cities'] = [
        (26, 38, 30),   # a
        (75, 6, 55),    # b
        (3, 46, 66),    # c
        (73, 59, 75),   # d
        (37, 72, 7),    # e
        (42, 83, 67),   # f
        (21, 77, 91),   # g
        (80, 18, 4),    # h
    ]  # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def print_solution(manager, routing, assignment):
    """Prints assignment on console."""
    names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    print('Objective: {} miles'.format(assignment.ObjectiveValue() / 100 ))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(names[manager.IndexToNode(index)])
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(names[manager.IndexToNode(index)])
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['cities']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = data['cities'][manager.IndexToNode(from_index)]
        to_node = data['cities'][manager.IndexToNode(to_index)]

        x1, y1, z1 = from_node
        x2, y2, z2 = to_node
        return round(math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2) * 100)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        print_solution(manager, routing, assignment)


if __name__ == '__main__':
    main()

