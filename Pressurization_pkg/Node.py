class Node:
    def __init__(self,m_dot=None,P=None):
        self.m_dot = m_dot
        self.P = P

    def __repr__(self):
        return 'Node object with\n\tm_dot = '+str(self.m_dot)+' kg/s\n\tP = '+str(self.P)+' Pa\n'

    def set(self,m_dot=None,P=None):
        if m_dot != None:
            self.m_dot = m_dot
        if P != None:
            self.P = P

