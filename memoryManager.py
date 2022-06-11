# Implementation of a program that simulates a memory manager
# that implements the buddy system. This program has the following characteristics:
# (a) When invoked, it will receive as an argument the number of memory blocks that it will handle.
# (b) Once the program is started, it will repeatedly ask the user for an action to proceed. Such action may be:
# i. RESERVE <name> <quantity>.
# Represents a space reservation of <quantity> blocks, associated with the identifier <name>.
# The program should report an error and ignore the action if <name> already has
# reserved memory or there is no contiguous free space large enough to satisfy the request (in either case
# to satisfy the request (in either case, the error message must be clear and informative).
# clear and informative).
# ii. FREE <name>
# Represents a release of the space containing the <name> identifier.
# The program must report an error and ignore the action if <name> does not have
# reserved memory (the error message must be clear and informative).
# iii. DISPLAY
# Must display a graphical representation (in text) of the free block lists,
# as well as the name information and the memory they have associated with them.
# iv. EXIT
# Should exit the simulator. At the end of the execution of each action,
# the program request the following action from the user.

from math import floor, ceil, log2


class MemoryManager:

    def __init__(self, memory_blocks: int):
        # verified that the memory_blocks is positive integer
        if not isinstance(memory_blocks, int) or memory_blocks < 1:
            raise ValueError("Memory blocks must be a integer greater than 0")

        # verified that the memory_blocks is a power of two
        if log2(memory_blocks) - int(log2(memory_blocks)) != 0:
            print("The program is not prepare to manage a number of blocks that is not a power of two")
            raise ValueError("Memory blocks must be a power of two")

        max_power_of_two = ceil(log2(memory_blocks))

        # Array track all the free nodes of various sizes
        list_of_blocks = [[]]
        for i in range(max_power_of_two):
            list_of_blocks += [[]]
        list_of_blocks[max_power_of_two].append((0, memory_blocks - 1))
        self.listOfBlocks = list_of_blocks
        self.memoryBlocks = memory_blocks
        self.listOfNames = {}

    def begin_program(self):
        memory_blocks = self.memoryBlocks
        print("\nWelcome to the Memory Manager")
        print("You have {} memory blocks\n".format(memory_blocks))
        self.memoryBlocks = memory_blocks

        # Main loop of the interactive program
        while True:
            action = input("Enter an action: ")
            param = action.split(" ")
            first_param = param[0].upper()
            if first_param == "RESERVE" or first_param == "RESERVAR" or first_param == "1":
                if len(param) == 3 and param[2].isdigit():
                    if param[1] not in self.listOfNames:
                        self.allocate(param[1], int(param[2]))
                    else:
                        print("Error: name already exists")
                else:
                    print("Error: invalid parameters")

            elif first_param == "FREE" or first_param == "LIBERAR" or first_param == "2":
                if len(param) == 2:
                    if param[1] in self.listOfNames:
                        self.free(param[1])
                    else:
                        print("Error: name does not exist")
                else:
                    print("Error: invalid number of parameters")

            elif first_param == "DISPLAY" or first_param == "MOSTRAR" or first_param == "3":
                self.display()

            elif first_param == "EXIT" or first_param == "SALIR" or first_param == "4":
                break

            else:
                print("Error: invalid action")

    def allocate(self, name: str, quantity: int):
        listOfBlocks = self.listOfBlocks

        # Verify that the quantity is a positive integer
        if not isinstance(quantity, int) or quantity < 1:
            print("Error: quantity must be a positive integer")
            return

        # Find the first free block of the right size
        listToFit = floor(ceil(log2(quantity)))

        # We already have such a block
        if len(listOfBlocks[listToFit]) != 0:
            # Remove the block from the list of free blocks
            allocatedBlock = listOfBlocks[listToFit].pop(0)
            # Add the block to the list of allocated blocks with the name
            self.listOfNames[name] = allocatedBlock
            print("\nBlock {} allocated in {}\n".format(name, allocatedBlock))
            return

        i = listToFit + 1
        # If not, search for a larger block
        while i < len(listOfBlocks) and len(listOfBlocks[i]) == 0:
            i += 1

        if i == len(listOfBlocks):
            print("\nError: no space available\n")
            return

        # Remove the block from the list of free blocks
        blockToSplit = listOfBlocks[i].pop(0)
        i -= 1

        # Split the block in two parts and add them to the list of free blocks
        # The first part is the block to split or to allocate and the second part is the new free block
        while i >= listToFit:
            lowerBound = blockToSplit[0]
            upperBound = blockToSplit[1]
            newBlock = (lowerBound, lowerBound + (upperBound - lowerBound) // 2)
            newBlock2 = (lowerBound + (upperBound - lowerBound + 1) // 2, upperBound)

            listOfBlocks[i].append(newBlock)
            listOfBlocks[i].append(newBlock2)

            blockToSplit = listOfBlocks[i].pop(0)
            i -= 1

        print("\nBlock {} allocated in {}\n".format(name, blockToSplit))

        self.listOfNames[name] = blockToSplit

    def free(self, name: str):
        listOfBlocks = self.listOfBlocks
        listOfNames = self.listOfNames

        # Invalid name
        if name not in self.listOfNames:
            print("Error: invalid free request, the name: {} is not allocated".format(name))
            return

        lowerBound = listOfNames[name][0]
        upperBound = listOfNames[name][1]
        sizeOfBlock = upperBound - lowerBound + 1

        # Get the list which will track free blocks of this size
        listToFree = int(ceil(log2(sizeOfBlock)))
        listOfBlocks[listToFree].append((lowerBound, lowerBound + (int(2 ** listToFree) - 1)))
        print("\nBlock freed")
        print("Block {}: {}\n".format(name, listOfNames[name]))

        # Calculate it's buddy number and buddyAddress.
        buddyNumber = lowerBound / sizeOfBlock

        if buddyNumber % 2 != 0:
            buddyAddrs = lowerBound - int(2 ** listToFree)
        else:
            buddyAddrs = lowerBound + int(2 ** listToFree)

        i = 0
        # Search in the free list for buddy
        while i < len(listOfBlocks[listToFree]):

            # This indicates the buddy is also free
            if listOfBlocks[listToFree][i][0] == buddyAddrs:

                # Buddy is the block after block with this base address
                if buddyNumber % 2 == 0:
                    # Add to appropriate free list
                    listOfBlocks[listToFree + 1].append((lowerBound, lowerBound + (int(2 ** listToFree) - 1)))
                    print("Coalescing of blocks starting at " + lowerBound + " and " + buddyAddrs + " was done\n")

                # Buddy is the block before block with this base address
                else:
                    # Add to appropriate free list
                    listOfBlocks[listToFree + 1].append((buddyAddrs, buddyAddrs + 2 * int(2 ** listToFree) - 1))
                    print("Coalescing of blocks starting at " + str(buddyAddrs) +
                          " and " + str(lowerBound) + " was done\n")
                # Remove the block from the list of free blocks
                listOfBlocks[listToFree].pop(i)
                listOfBlocks[listToFree].pop()
                break
            i += 1

        listOfNames.pop(name)

    # Show graphical representation of the memory
    def display(self):
        print("\nFree blocks of memory allowed:")
        print("List of blocks: {}".format(self.listOfBlocks))
        print("Names of allocate blocks: associated memory")
        print("List of names: {}\n".format(self.listOfNames))

