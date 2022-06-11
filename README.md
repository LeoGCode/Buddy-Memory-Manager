# Buddy-Memory-Manager
Implementation of a program that simulates a memory manager that implements the buddy system

This program has the following characteristics:

- When invoked, it will receive as an argument the number of memory blocks that it will handle.

- Once the program is started, it will repeatedly ask the user for an action to proceed. Such action may be:
    * RESERVE \<name> \<quantity>.
Represents a space reservation of \<quantity> blocks, associated with the identifier \<name>.
The program report an error and ignore the action if <name> already has reserved memory or there
is no contiguous free space large enough to satisfy the request.
  
    * FREE \<name>
Represents a release of the space containing by \<name> identifier.
The program report an error and ignore the action if <name> does not have
reserved memory.
  
    * DISPLAY
 Display a graphical representation (in text) of the free block lists,
as well as the name information and the memory they have associated with them.
  
    * EXIT
Exit the simulator. At the end of the execution of each action,
the program request the following action from the user.
