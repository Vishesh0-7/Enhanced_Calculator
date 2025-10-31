from app.calculator_memento import Caretaker


def test_caretaker_save_undo_redo():
    c = Caretaker()
    state1 = [1]
    state2 = [1, 2]
    c.save(state1)
    c.save(state2)
    # undo to state2 then state1
    new = c.undo(state2)
    assert new == state2 or new == state1
    # calling redo/undo maintain stacks (basic smoke test)
    _ = c.redo(new)
