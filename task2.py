def zfc(string):
    binary_mask = 0  
    last_show_place = [-1] * 26
    output = ""
    for i in range(len(string)):
        char = string[i]
        binary_position = 1 << (ord(char) - ord('a')) 
        last_show_place[(ord(char) - ord('a'))] = i
        if ((binary_mask & binary_position) != 0):  
            output += "-"
        else:
            output += char

        if (i >= 10 and last_show_place[(ord(string[i - 10]) - ord('a'))] == (i - 10)):  
            binary_mask ^= 1 << (ord(string[i - 10]) - ord('a'))

        binary_mask |= binary_position  

    return output


input1 = "abcdefaxc"
output1 = zfc(input1)
print(output1)  #abcdef-x-

input2 = "abcdefaxcqwertba"
output2 = zfc(input2)
print(output2)  #abcdef-x-qw-rtb-