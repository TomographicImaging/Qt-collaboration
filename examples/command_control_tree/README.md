# WHAT IS THIS EXAMPLE AND HOW TO USE IT

This is a piece of code that has almost the same functionality of the command control tree in [Dui2](https://github.com/ccp4/DUI2/)

This is a starting point and I tried to make it as simple as it gets. The idea here is to have available some tools that can be used separately.

These are the tree ways you can run the program(s) on your own:

1. Fully local CLI app (single process without GUI that only includes the core of the control tree)

       python3 tree_nav.py

2. Fully local GUI app (single process that includes the core of the control tree and the GUI)

       python3 all_local_gui.py

3. Server and Client App (GUI talking to a Server, the core of the control tree is in the server side)

you should run two different programs, technically they can be in different computers but you will need to edit the URL in both:

       python3 http_server_w_cors.py

and

       python3 client_gui.py

Depending on your project needs, feel free to take any module you want and edit it as you see fit. Don't be shy to contact [Luiso](https://github.com/luisodls) for guidance on how to re-use this code.




