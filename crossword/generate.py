import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())



    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Create a deep copy of the self.domains dict
        alt_domains = copy.deepcopy(self.domains)
        # Loop through the domain
        for var in self.domains:
            # Loop through the variable's values
            for value in self.domains[var]:
                # Check if the value is consistent with the unary constraints
                if len(value) != var.length:
                    # If not remove that va lue
                    alt_domains[var].remove(value)

        # Update self.domains
        self.domains = alt_domains


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Initialize the return value as False
        return_value = False

        overlap = self.crossword.overlaps[x, y]
        to_remove = set() # alt_domains = copy.deepcopy(self.domains)

        # If there is overlap, store the position of the overlapping character
        if overlap:
            i, j = overlap

            # Loop through x's domain
            for x_value in self.domains[x]:
                condition = False  # Initialize the condition as False
                # Loop through y's domain
                for y_value in self.domains[y]:
                    # Check if the overlapping character differs between the values
                    if x_value[i] == y_value[j]:
                        condition = True
                        break
                if not condition:
                    to_remove.add(x_value)
                    return_value = True

        # Remove any domain variables that aren't arc consistent:
        self.domains[x] = self.domains[x] - to_remove

        return return_value


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with the initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # Check if 'arcs' is None
        if arcs is None:
            # Create a list containing all arcs
            arcs = []
            for x in self.domains.keys():
                for y in self.domains.keys():
                    if x != y:
                        arcs.append((x, y))

        # While arcs is not empty
        while arcs:
            # Unpack the tuple
            x, y = arcs.pop()

            # Check if the tuple is arc consistent
            if self.revise(x, y):
                # Check if the domain of x is empty
                if not self.domains[x]:
                    return False

                    # Loop through the neighbors of x
                    for z in self.crossword.neighbors(x):
                        if z != y:
                                # Add tuple to the queue
                                arcs.append((z, x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # Loop through the domain and check if the assignment is complete
        for var in self.domains.keys():
                if var not in assignment.keys():
                    return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check for distinct values
        seen_values = set()
        for key, x_value in assignment.items():
            if x_value in seen_values:
                return False

            seen_values.add(x_value)

            # Check that every value have the correct lenght
            if key.length != len(x_value):
                return False

            # Check for conflicts between neighboring variables
            neighbors = self.crossword.neighbors(key)
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[key, neighbor]
                if overlap is not None:
                    i, j = overlap
                    if neighbor in assignment:
                        y_value = assignment[neighbor]

                        # Check if the overlaping character differs between the values
                        if x_value[i] != y_value[j]:
                            return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Initialize an empty list to store values and their impact counts
        lcv_values = []

        # Get unassigned neighboring variables of 'var'
        unassigned_neighbors = [neighbor for neighbor in self.crossword.neighbors(var) if neighbor not in assignment]

        # Loop through var values
        for value in self.domains[var]:
            # Initialize a counter for the number of values ruled out
            impact_count = 0

            # Check each unassigned neighboring variable
            for neighbor in unassigned_neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                if overlap is not None:
                    i, j = overlap
                    for neighbor_value in self.domains[neighbor]:
                        if value[i] != neighbor_value[j]:
                            impact_count += 1

            # Add the value and its impact count to the list
            lcv_values.append((value, impact_count))

        # Sort the list in ascending order of impact counts (least impact first)
        lcv_values.sort(key=lambda x: x[1])

        # Extract and return the values from the sorted list
        sorted_values = [value for value, _ in lcv_values]

        return sorted_values


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Initialize an empty list to store variables
        unnasigned_variables = []

        # Find all unassigned variables
        for variable in self.domains.keys():
            if variable not in assignment.keys():
                unnasigned_variables.append(variable)

        # Sort the variables based on the minimum remaining values and degree
        unnasigned_variables.sort(
            key=lambda x: (len(self.domains[x]), -len(self.crossword.neighbors(x)))
        )

        # Return the first element of the list
        return unnasigned_variables[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # Check if assignment is complete and consistent. If so return assignment
        if self.assignment_complete(assignment):
            return assignment

        # Otherwise select an unnasigned variable
        variable = self.select_unassigned_variable(assignment)

        # Loop through the values of the selected variable domains
        for value in self.order_domain_values(variable, assignment):

            # Assign the value to the variable
            assignment[variable] = value

            # Check consistency
            if self.consistent(assignment):
                # Recursively search
                result = self.backtrack(assignment)

                if result:
                    # Return the solution
                    return result

                del assignment[variable]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
