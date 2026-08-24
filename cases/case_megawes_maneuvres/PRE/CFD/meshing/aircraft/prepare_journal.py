
#NOTES:
# - All components are complete (no halves)
# - Local origin is at the leading edge in the middle of the component (except ailerons: original frame wing)
# - Rudder already rotated
# - CHECK ID's!

#File names
input_file = "make_aircraft.jou"
output_file = "make_aircraft_ready.jou"
input_name_aileron =  "/cfdfile1/data/fm/niels/awesim/case_systemID/PRE/CFD/meshing/aircraft/Aileron.cas.h5"
input_name_aileron2 = "Aileron.cas.h5"
input_name_wing =  "Wing_hole_coarse.cas.h5"
input_name_rudder = "VTail_overset.cas.h5"
input_name_elevator = "Tail_overset.cas.h5"
output_name_aircraft = "aircraft.cas.h5"

#Settings Aircraft (input in strings)
delta_a = "0"   #RAD #OPPOSITE SIGN!
delta_e = "0"   #SAME SIGN
delta_r = "0"  #OPPOSITE SIGN!

y_scale_wing = "1.0"
cg_x = "-1.67" #Translation wing
cg_z = "-0.229"

aileron_right_origin_x =  "2.742"  #"2.7775" #IN LE FRAME!
aileron_right_origin_y =  "13.17"  #"12.85"
aileron_right_origin_z =   "0.186" #"0.09454"
aileron_right_axis_x =   "0.532" #"0.4275"
aileron_right_axis_y =  "-7.07"  #"-6.175"
aileron_right_axis_z =  "0.057"  #"-0.0341"

aileron_left_origin_y =  "-13.17" #"-12.85"
aileron_left_axis_y =  "7.07" #"6.175"

rudder_right_pos_x = "9.03" #IN CG FRAME!
rudder_right_pos_y = "3.8"
rudder_right_pos_z = "1.771" #2 : Dz = 0.5
rudder_right_origin_x = "9.73"
rudder_right_origin_y = "3.8"
rudder_right_origin_z =  "0"
rudder_left_pos_y = "-3.8"
rudder_left_origin_y = "-3.8"
elevator_pos_z =  "-0.229"
elevator_pos_y = "0"
elevator_origin_y = "0"
elevator_origin_z = "-0.229"

#Aircraft initial position and attitude
Rx = "0" #RAD
Ry = "0"
Rz = "0"
Pos_x = "0"
Pos_y = "0"
Pos_z = "0"

def replace_words_in_file(input_file, output_file, replacements):
    try:
        with open(input_file, 'r') as file:
            content = file.read()

        for old_word, new_word in replacements.items():
            content = content.replace(old_word, new_word)

        with open(output_file, 'w') as file:
            file.write(content)

        print("Replaced words and saved the result to {}".format(output_file))

    except FileNotFoundError:
        print("File '{}' not found.".format(input_file))
    except Exception as e:
        print("An error occurred: {}".format(str(e)))

# Usage example:
if __name__ == "__main__":

    # Define your replacements as a dictionary, where keys are old words and values are new words.
    replacements = {
        "|INPUT_NAME_AILERON|": input_name_aileron,
        "|INPUT_NAME_AILERON2|": input_name_aileron2,
        "|INPUT_NAME_WING|": input_name_wing,
        "|DELTA_A|": delta_a,
        "|Y_SCALE_WING|": y_scale_wing,
        "|CG_X|": cg_x,
        "|CG_Z|": cg_z,
        "|AILERON_RIGHT_ORIGIN_X|" : aileron_right_origin_x,
        "|AILERON_RIGHT_ORIGIN_Y|": aileron_right_origin_y,
        "|AILERON_RIGHT_ORIGIN_Z|": aileron_right_origin_z,
        "|AILERON_RIGHT_AXIS_X|": aileron_right_axis_x,
        "|AILERON_RIGHT_AXIS_Y|": aileron_right_axis_y,
        "|AILERON_RIGHT_AXIS_Z|": aileron_right_axis_z,
        "|AILERON_LEFT_AXIS_Y|": aileron_left_axis_y,
        "|AILERON_LEFT_ORIGIN_Y|": aileron_left_origin_y,
        "|INPUT_NAME_RUDDER|": input_name_rudder,
        "|RUDDER_RIGHT_POS_X|": rudder_right_pos_x,
        "|RUDDER_RIGHT_POS_Y|": rudder_right_pos_y,
        "|RUDDER_RIGHT_POS_Z|": rudder_right_pos_z,
        "|DELTA_R|": delta_r,
        "|RUDDER_RIGHT_ORIGIN_Z|": rudder_right_origin_z,
        "|RUDDER_RIGHT_ORIGIN_Y|": rudder_right_origin_y,
        "|RUDDER_RIGHT_ORIGIN_X|": rudder_right_origin_x,
        "|RUDDER_LEFT_POS_Y|": rudder_left_pos_y,
        "|RUDDER_LEFT_ORIGIN_Y|": rudder_left_origin_y,
        "|INPUT_NAME_ELEVATOR|": input_name_elevator,
        "|ELEVATOR_POS_Z|": elevator_pos_z,
        "|ELEVATOR_POS_Y|": elevator_pos_y,
        "|DELTA_E|": delta_e,
        "|ELEVATOR_ORIGIN_Y|": elevator_origin_y,
        "|ELEVATOR_ORIGIN_Z|": elevator_origin_z,
        "|OUTPUT_NAME_AIRCRAFT|": output_name_aircraft,
        "|RX|": Rx,
        "|RY|": Ry,
        "|RZ|": Rz,
        "|POS_X|": Pos_x,
        "|POS_Y|": Pos_y,
        "|POS_Z|": Pos_z,
    }

    replace_words_in_file(input_file, output_file, replacements)
