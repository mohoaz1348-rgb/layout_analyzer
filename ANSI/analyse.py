from pathlib import Path
import copy
languages_list = ['en', 'ru']
range_list = ['-3','-2','-1','0','1','2','3','alt','not_found']
results_table_caption = ['layout']
for x in range_list:
    results_table_caption.append(x)

left_std_list = []
left_std_file = open('left')
for x in left_std_file:
    left_std_list.append(x.split())
#print(left_std_list)
left_std_file.close()

left_angle_list = []
left_angle_file = open('left_angle')
for x in left_angle_file:
    left_angle_list.append(x.split())
#print(left_angle_list)
left_angle_file.close()

right_list = []
right_file = open('right')
for x in right_file:
    right_list.append(x.split())
#print(right_list)
right_file.close()



for lang in languages_list:

    results_table = []
    results_table.append(results_table_caption)
    bigrams_list = []
    bigrams_file = open('./' + lang + '/bigrams')
    for x in bigrams_file:
        bigrams_list.append(x.split())
    #print(bigrams_list)
    bigrams_file.close()
    
    results_full_file = open('./' + lang + '/results_full', 'w')
    directory_path = Path('./' + lang + '/layouts')

    for file_path in directory_path.iterdir():
        if file_path.is_file():

            results_string = []
            layout_list = []
            layout_file = open(file_path)
            file_name = file_path.name
            #print(file_name)
            results_string.append(file_name)

            i = 0
            for x in layout_file:
                i = i + 1
                if i == 4:
                    break
                layout_list.append(x.rstrip('\n'))
            #print(layout_list)
            layout_file.close()

            i = 0
            result_list = copy.deepcopy(bigrams_list)
            #print(result_list)

            left_list = []
            if layout_list[0] == 'angle':
                left_list = copy.deepcopy(left_angle_list)
            elif layout_list[0] == 'std':
                left_list = copy.deepcopy(left_std_list)
            else:
                print("You must classify layout as 'angle' or 'std'")
            for x in bigrams_list:
                bigram = x[0].lower()
                if ((bigram[0] in layout_list[1]) and (bigram[1] in layout_list[1])):
                    pos_i = layout_list[1].find(bigram[0])
                    pos_j = layout_list[1].find(bigram[1])
                    if ((pos_i != -1) and (pos_j != -1)):
                        result_list[i].append(left_list[pos_i][pos_j])
                    else:
                        result_list[i].append('not_found')
                elif ((bigram[0] in layout_list[2]) and (bigram[1] in layout_list[2])):
                    pos_i = layout_list[2].find(bigram[0])
                    pos_j = layout_list[2].find(bigram[1])
                    if ((pos_i != -1) and (pos_j != -1)):
                        result_list[i].append(right_list[pos_i][pos_j])
                    else:
                        result_list[i].append('not_found')
                elif ((bigram[0] in layout_list[1]) and (bigram[1] in layout_list[2])):
                    result_list[i].append('alt')
                elif ((bigram[0] in layout_list[2]) and (bigram[1] in layout_list[1])):
                    result_list[i].append('alt')
                else:
                    result_list[i].append('not_found')
                i = i + 1
            print('')
            print(file_name.upper())
            results_full_file.write('\n')
            results_full_file.write(file_name.upper() + '\n')
            #print(result_list)

            stat_list = []
            for x in range_list:
                sum = 0.000
                i = 0
                bigrams_string = ''
                print(x + '(' + file_name + ')')
                results_full_file.write(x + '(' + file_name + ')' + '\n')
                for y in result_list:
                    if (y[2] == x):
                        #print(y)
                        i = i + 1
                        bigram_str = y[0] + '=' + y[1]
                        bigrams_string = bigrams_string + f"{bigram_str:<{10}}"
                        if i == 10:
                            print(bigrams_string)
                            results_full_file.write(bigrams_string + '\n')
                            bigrams_string = ''
                            i = 0
                        sum = sum + float(y[1])
                print(bigrams_string)
                print('')
                results_full_file.write(bigrams_string + '\n')
                results_full_file.write('\n')
                stat_list.append([x,round(sum, 3)])
            
            for x in stat_list:
                #print(x)
                results_string.append(x[1])
            results_table.append(results_string)
    
    results_file = open('./' + lang + '/results', 'w')
    fixed_length = 10

    for x in results_table:
        z = ''
        i = 0
        for y in x:
            i = i + 1
            if i == 1:
                z = z + f"{str(y):<{fixed_length*2}}"
            else:
                z = z + f"{str(y):<{fixed_length}}"
        print(z)
        results_file.write(z + '\n')
    results_file.close()

