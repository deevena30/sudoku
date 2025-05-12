import numpy as np                                
import random
arr=np.zeros((9,9),dtype=int)
list_tuples=[(i,j) for i in range(9) for j in range(9)]
def print_sudoku(arr):
    for row in arr:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(f"{x}" for x in row) + " |")
    print("+---" * len(row) + "+")    

def safe_row(num, row, arr):
    return num not in arr[row]

def safe_column(num, col, arr):
    return num not in arr[:, col]

def is_box_good(arr, row, col, num):
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if arr[start_row + i][start_col + j] == num:
                return False
    return True     

def generate_sudoku(arr,i=0,j=0):
    if i>=9:
        return True
    if j >= 9:
       return generate_sudoku(arr, i + 1, 0)  
    if arr[i][j]!=0:
        return generate_sudoku(arr, i, j + 1)   
    digits=np.random.permutation(np.arange(1,10,1))
    for num in digits:
         if safe_row(num,i,arr) and safe_column(num,j,arr) and is_box_good(arr,i,j,num):
           arr[i][j]=num
           if generate_sudoku(arr,i,j+1):
              return True
           arr[i][j]=0
    return False    



def validate_sudoku(arr, row, column):
    if arr[row][column] != 0:
        current_value = arr[row][column]
        arr[row][column] = 0
        valid = safe_row(current_value, row, arr) and safe_column(current_value, column, arr) and is_box_good(arr, row, column, current_value)
        arr[row][column] = current_value
        return valid
    return True          

generate_sudoku(arr)
n=np.random.choice(np.arange(17,40,1))
sudoku_initial_positions = random.sample(list_tuples,n)
for i in sudoku_initial_positions:
    arr[i[0]][i[1]]=0

game_over=True
n=3
print_sudoku(arr)
while(True):
    if n==0:
       print("")
       print("")
       print("game over*")
       break
    row=int(input("Enter row no from 1-9: "))
    if(row>9 or row<=0):
        print("row no cannot be outside 1-9")
        continue
    column=int(input("Enter column no from 1-9: "))
    if(column>9 or column<=0):
        print("col no cannot be outside 1-9")
        continue
    row-=1
    column-=1
    if arr[row][column]!=0:
        print("cannot change a fixed value")
        continue
    value=int(input("Enter value to enter in the cell: "))
    arr[row][column]=value
    if not validate_sudoku(arr,row,column):
       print_sudoku(arr)
       n-=1
       print("That's a wrong move")
       print(n," more tries") 
       print("")
       print("better luck in next move")
       print("")
       arr[row][column]=0
       print_sudoku(arr)
    else:
         print_sudoku(arr)
         print("that's a correct one ")
         print("you still got ",n,"wrong moves")