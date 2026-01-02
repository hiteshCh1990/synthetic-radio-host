from engine import generate_radio_show_from_script

def test_script_parsing():
    script = """
    Anjli: Hello dosto
    Hitesh: Hi Anjli
    """
    output = generate_radio_show_from_script(script)
    assert output.endswith(".mp3")