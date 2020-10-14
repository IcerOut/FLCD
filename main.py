from SymbolTable import SymbolTable

if __name__ == '__main__':
    st = SymbolTable()
    val_1 = st.add_symbol('identifier_1')
    val_2 = st.add_symbol('constant_2')
    assert val_1 == 1
    assert val_2 == 2
    val_duplicate_1 = st.add_symbol('identifier_1')
    assert val_duplicate_1 == val_1
    val_3 = st.add_symbol('identifier_3')
    assert val_3 == 3

    val_result_1 = st.search_symbol('identifier_1')
    assert val_result_1 == 1
    val_result_2 = st.search_symbol('constant_2')
    assert val_result_2 == 2
    val_result_3 = st.search_symbol('identifier_3')
    assert val_result_3 == 3
    val_result_invalid = st.search_symbol('constant_4')
    assert val_result_invalid == -1

    print('All assertions were correct, all tests passed!')