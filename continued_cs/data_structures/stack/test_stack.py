from continued_cs.data_structures.stack import Stack


class TestStack:
    def test_stack_is_empty(self):
        st = Stack()
        assert st.is_empty()

    def test_stack_non_empty(self):
        st = Stack()
        st.push(3)
        assert not st.is_empty()

    def test_stack_pop(self):
        st = Stack()
        st.push(5)
        assert st.pop() == 5

    def test_stack_peek(self):
        st = Stack()
        st.push(7)
        assert st.peek() == 7
        assert not st.is_empty()

    def test_stack_end_to_end(self):
        st = Stack()
        st.push(7)
        assert st.peek() == 7
        st.push(3)
        assert st.pop() == 3
        st.push(5)
        assert st.peek() == 5
        assert st.pop() == 5
        assert st.pop() == 7
        assert st.is_empty()
