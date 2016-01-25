from util import parse_light_control_file

filename = "example.light_control"
commands = parse_light_control_file(filename)
print "Commands:"
print commands