class Input:

    def up(self):
        parent.rpc.request('Input.Up')

    def down(self):
        parent.rpc.request('Input.Down')

    def left(self):
        parent.rpc.request('Input.Left')

    def right(self):
        parent.rpc.request('Input.Right')

    def select(self):
        parent.rpc.request('Input.Select')

    def back(self):
        parent.rpc.request('Input.Back')

    def home(self):
        parent.rpc.request('Input.Home')

    def context_menu(self):
        parent.rpc.request('Input.ContextMenu')

    def input(self):
        parent.rpc.request('Input.Info')
