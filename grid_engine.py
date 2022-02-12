import pgwidget.pgwidget_core as pgw
import pygame





glc=pgw.GuiLayoutContext()

geh=pgw.GuiEventHandler(glc)

gth=pgw.GuiTimeHandler(glc,geh)


def click_grid(pos):
    #print("CLICK BUTTON")
    for i,grid in enumerate(grids.elements):
        if grid.is_point_in_rectangle(pos):
            grid.on_click(pos)
    

grid1=pgw.Grid([50,50], [15,15], 35, 60)




import random


starting_coor=((0,0),0) #coordinates, step distance



WALL_COLOR=(200,200,200)

for i in range(1000):
    a=random.randint(0,len(grid1.table_cells)-1)

    grid1.table_cells[a].color=WALL_COLOR



PASSAGE_COLOR=(100,250,100)
USED_COLOR=(250,100,100)
coordinates_list=[starting_coor]
coordinates=coordinates_list[0]

def find_next_steps():
    global coordinates #start coordinates
    
    row,col=coordinates[0]
    index=grid1.find_cell_index(row, col)
    grid1.table_cells[index].color=USED_COLOR
    
    global coordinates_list
    new_coor=[]
    new_coor.append(((coordinates[0][0]+1,coordinates[0][1]),coordinates[1]+1))
    new_coor.append(((coordinates[0][0]-1,coordinates[0][1]),coordinates[1]+1))
    new_coor.append(((coordinates[0][0],coordinates[0][1]+1),coordinates[1]+1))
    new_coor.append(((coordinates[0][0],coordinates[0][1]-1),coordinates[1]+1))
    
    #Check for boundaries
    for i,coor in enumerate(new_coor):
        row,col=coor[0]
        if min(row,col)<0: #negative side
            new_coor.remove(coor)
        if row>=grid1.rows or col>=grid1.cols:
            new_coor.remove(coor)
        
            
    
    
    
    #Check for obstacles and used tiles
    for i,coor in enumerate(new_coor):
        row,col=coor[0]
        index=grid1.find_cell_index(row, col)
        if str(grid1.table_cells[index].color)==str(WALL_COLOR):
            print("WALL", coor[0])
            new_coor.remove(coor)
        
    #Check for obstacles and used tiles
    for i,coor in enumerate(new_coor):
        row,col=coor[0]
        index=grid1.find_cell_index(row, col)
        if str(grid1.table_cells[index].color)==str(USED_COLOR):
            print("USED", coor[0])
            new_coor.remove(coor)
            
            
    
    #Check for duplicate
    for i,coor in enumerate(new_coor):
        if str(coor[0]) in [str(x[0]) for x in coordinates_list]:
            print("REMOVING", coor[0])
            new_coor.remove(coor)
            
    print(new_coor)
    coordinates_list+=new_coor
    #print(coordinates_list)
    for coordinates in new_coor:
        row,col=coordinates[0]
        index=grid1.find_cell_index(row, col)
        grid1.table_cells[index].color=PASSAGE_COLOR
    
    

counter=0

def run_iteration():
    global counter
    global coordinates
    coordinates=coordinates_list[counter]
    find_next_steps()
    counter+=1


    
#trigger1=pgw.TimeTrigger(10,run_iteration)

#gth.time_triggers.append(trigger1)


grids=pgw.PgWidget(click_grid)
grids.elements.append(grid1)

grid1.table_cells[1].color=WALL_COLOR

pgwidgets=[grids]
 



glc.pgwidgets=pgwidgets




def main_program_loop(glc,geh,gth):
    """GuiLayoutContext,GuiEventHandler,GuiTimeHandler"""
    done=False
    t=0
    new_select_possible=True
    selected=None
    
   
                
    while not done:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1: #Left button of mouse
                    geh.handle_left_click()                                
                                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button==3: #Right button of mouse
                    geh.handle_right_click(event)
                             
                elif event.type == pygame.MOUSEBUTTONUP:
                    geh.handle_unclick()
                                    
                elif event.type == pygame.MOUSEMOTION:                
                    for i,table in enumerate(glc.tables):
                        if geh.actively_selected_draggable_component==table:
                            geh.drag_table(table,event)
                    
                    for i,rect in enumerate(glc.rects+glc.entries):
                        if geh.actively_selected_draggable_component==rect:
                            geh.drag_rect(rect,event)
                            
                elif event.type == pygame.KEYDOWN:
                    geh.handle_key_down(event)
                    
                    
                elif event.type == pygame.KEYUP: 
                    geh.handle_key_up(event)
            
                elif event.type == pygame.QUIT:
                    done = True
            
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                       
            pygame.display.flip()   
    
        except KeyboardInterrupt:
            pygame.display.quit()
            pygame.quit()
           
        gth.tick()
      
    pygame.display.quit()
    pygame.quit()
   

main_program_loop(glc, geh, gth)
