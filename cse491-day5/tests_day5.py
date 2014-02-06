import day5

def test_add_2_numbers():
    x = day5.add_2_numbers(2, 2)
    assert x == 4, x

def test_add_2_numbers_2():
    x = day5.add_2_numbers(15, 20)
    assert x == 35, x

def test_divide_2_numbers():
    x = day5.divide_2_numbers(6, 3)
    assert x == 2, x

def test_divide_2_numbers_float():
    x = day5.divide_2_numbers(7, 3)
    assert round(x, 1) == 2.3, x

def test_get_3rd_value():
    x = day5.get_3rd_value("a,b,c,d,e,f")
    assert x == "c", x

def test_get_4th_comma_plus():
    x = day5.get_4th_comma_plus("a,b,c,d,e,f,g")
    assert x == "e,f,g", x

def test_get_lines_4_5():
    x = day5.get_lines_4_5("a\nb\nc\nd\ne\nf\n")
    assert x == ["d", "e"], x

def test_get_cleaned_values_3_4():
    x = day5.get_cleaned_values_3_4("_a,_b,_c,_d,_e,_f")
    assert x == ["d", "e"], x
