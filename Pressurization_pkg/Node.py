class Node:
    def __init__(self,m_dot=None,p_t=None):
        self.m_dot = m_dot
        self.p_t = p_t
        self.p_upstream = None
        self.p_downstream = None

    def __repr__(self):
        return 'Node object with\n\tm_dot = '+str(self.m_dot)+' kg/s\n\tp = '+str(self.p_t)+' Pa\n\tp_upstream = '+str(self.p_upstream)+' Pa\n\tp_downstream = '+str(self.p_downstream)

    def set(self,m_dot=None,p_t=None,p_upstream=None,p_downstream=None):
        if m_dot != None:
            self.m_dot = m_dot
        if p_t != None:
            self.p_t = p_t
        if p_upstream != None:
            self.p_upstream = p_upstream
        if p_downstream != None:
            self.p_downstream = p_downstream

