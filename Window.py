import numpy as np
import mathutils

RIGHT_ANGLE = 1.5707963705062866

class Window:
    def __init__(self, vert0):
        self.vert0 = vert0
        
        #look for vert4 and calculate normal
        for edge in self.vert0.link_edges:
            vert_assess = edge.other_vert(self.vert0)
            #CASE: vert4
            if edge.calc_length() == 0.5 and vert_assess.co.z == self.vert0.co.z:
                self.vert4 = vert_assess
                self.window_normal = 2 * (vert_assess.co - self.vert0.co)
            
       #CASE: Data so far is not valid
        if not hasattr(self, 'vert4'):
            raise Exception('Not valid window (no Vert4)')
        
        #look for verts 1 & 2
        for edge in vert0.link_edges:
            vert_assess = edge.other_vert(self.vert0)
            
            #CASE: vert1 (same z & angle between vert0 -> vert1 == 90 degrees (PI/2 radians))
            if self.vert0.co.z == vert_assess.co.z and ( self.angle_to_normal(self.vert0, vert_assess) == RIGHT_ANGLE):
                self.vert1 = vert_assess;
                self.window_width_normal = (self.vert1.co - self.vert0.co)
                self.window_width_normal = self.window_width_normal.normalized()
            
            #CASE: vert2 (vert2 is on same z axis but is higher up)
            elif vert_assess.co.x == self.vert0.co.x and vert_assess.co.y == self.vert0.co.y and vert_assess.co.z > self.vert0.co.z:
                self.vert2 = vert_assess

        #CASE: Data so far is not valid
        if not hasattr(self, 'vert1') or not hasattr(self, 'vert2'):
            raise Exception('Not valid window (no Vert1 or Vert2)')
        
        #look for verts 5 & 6
        for edge in self.vert4.link_edges:
            vert_assess = edge.other_vert(self.vert4)
            
            #CASE: vert5 (same z & located 0.5 from vert1)
            if vert_assess.co.z == self.vert4.co.z and (vert_assess.co - self.vert1.co).length == 0.5:
                self.vert5 = vert_assess
            
            #CASE: vert6 (located 0.5 from vert2 at same z)
            elif vert_assess.co.z == self.vert2.co.z and (vert_assess.co - self.vert2.co).length == 0.5:
                self.vert6 = vert_assess
        
        
        #CASE: Data so far is not valid
        if not hasattr(self, 'vert5') or not hasattr(self, 'vert6'):
            raise Exception('Not valid window (no Vert5 or vert6)')
        
        #look for vert7
        for edge in self.vert5.link_edges:
            vert_assess = edge.other_vert(self.vert5)
            
            #CASE: vert7 (same z axis + same height)
            if vert_assess.co.x == self.vert5.co.x and vert_assess.co.y == self.vert5.co.y and vert_assess.co.z > self.vert5.co.z:
                self.vert7 = vert_assess
        
        #CASE: Data so far is not valid
        if not hasattr(self, 'vert7'):
            raise Exception('Not valid window (no Vert7)')
        
        #look for vert3
        for edge in self.vert1.link_edges:
            vert_assess = edge.other_vert(self.vert1)
            
            #CASE: vert3 (same z axis + same height)
            if vert_assess.co.x == self.vert1.co.x and vert_assess.co.y == self.vert1.co.y and vert_assess.co.z > self.vert1.co.z:
                self.vert3 = vert_assess
        
        #CASE: Data so far is not valid
        if not hasattr(self, 'vert3'):
            raise Exception('Not valid window (no Vert3)')
            
        
        self.is_door = self.is_window_door()
        
        
    def validate(self):
        return True
    
    def get_verts(self):
        if self.validate():
            return np.array([self.vert0, self.vert1, self.vert2, self.vert3, self.vert4, self.vert5, self.vert6, self.vert7])
        else:
            return np.array([])
        
    def angle_to_normal(self, vert1, vert2):
        edge = (vert2.co) - (vert1.co)
        return edge.angle(self.window_normal)
    
    def is_vertex_at_floor_level(self, primary, vert1, vert2, vert3):
        for edge in primary.link_edges:
            vert_assess = edge.other_vert(primary)
            
            if(vert_assess != vert1 and vert_assess != vert2 and vert_assess != vert3 and vert_assess.co.z == primary.co.z):
                return True
            
        return False
                
        
    def is_window_door(self):
        vert0_floor_level = self.is_vertex_at_floor_level(self.vert0, self.vert1, self.vert4, self.vert5)
        vert1_floor_level = self.is_vertex_at_floor_level(self.vert1, self.vert0, self.vert4, self.vert5)
        vert4_floor_level = self.is_vertex_at_floor_level(self.vert4, self.vert0, self.vert1, self.vert5)
        vert5_floor_level = self.is_vertex_at_floor_level(self.vert5, self.vert0, self.vert1, self.vert4)
        
        if (vert0_floor_level and vert1_floor_level) or (vert4_floor_level and vert5_floor_level):
            return True
        
        return False
        
        
    
    def generate_pane(self, bm):
        #this is gonna be fun lol, up to 32 tri's and each one manually cause monkey brain, maybe future Sam is smarter and has a good solution
        window_verts = self.get_verts()
        
        pane_verts = np.array([])
        
        #TODO calculate if a door or not
        
        
        
        #calculate 
        for i, vert in enumerate(window_verts):
            # 0,1,2,3 = -ve while 4,5,6,7 = +ve
            window_normal_factor = -1
            if i > 3:
                window_normal_factor = 1
                
            #even numbers = -ve while odd numbers = +ve
            window_width_normal_factor = 1
            if i % 2 == 0:
                window_width_normal_factor = -1
                
            #0,1,4,5 = -ve while 2,3,6,7 = +ve
            window_height_factor = 1
            if i == 0 or i == 1 or i == 4 or i == 5:
                window_height_factor = -1
                if self.is_door:
                    window_height_factor = 0
            
            
            #calculate outer
            outer_coords = vert.co + (0.1 * self.window_normal * window_normal_factor) 
            outer_coords = outer_coords + (0.1 * self.window_width_normal * window_width_normal_factor)
            outer_coords = outer_coords + (mathutils.Vector((0.0, 0.0, 0.1)) * window_height_factor)
            if window_height_factor == 0:
                outer_coords = outer_coords - mathutils.Vector((0.0, 0.0, 0.1))
            outer_coords = bm.verts.new(outer_coords)
            
            
            #calculate inner
            inner_coords = vert.co + (0.1 * self.window_normal * window_normal_factor)
            inner_coords = inner_coords - (0.1 * self.window_width_normal * window_width_normal_factor)
            inner_coords = inner_coords - (mathutils.Vector((0.0, 0.0, 0.1)) * window_height_factor)
            if window_height_factor == 0:
                inner_coords = inner_coords - mathutils.Vector((0.0, 0.0, 0.1))
            inner_coords = bm.verts.new(inner_coords)
            
            #Push calculated values to array
            pane_verts = np.append(pane_verts, outer_coords)
            pane_verts = np.append(pane_verts, inner_coords)
            
        #make faces (monkey brain incoming)
        bm.faces.new((pane_verts[0], pane_verts[4], pane_verts[12], pane_verts[8]))
        bm.faces.new((pane_verts[0], pane_verts[1], pane_verts[5], pane_verts[4]))
        bm.faces.new((pane_verts[6], pane_verts[7], pane_verts[3], pane_verts[2]))
        bm.faces.new((pane_verts[6], pane_verts[7], pane_verts[5], pane_verts[4]))
        bm.faces.new((pane_verts[6], pane_verts[2], pane_verts[10], pane_verts[14]))
        bm.faces.new((pane_verts[6], pane_verts[4], pane_verts[12], pane_verts[14]))
        bm.faces.new((pane_verts[11], pane_verts[3], pane_verts[7], pane_verts[15]))
        bm.faces.new((pane_verts[11], pane_verts[10], pane_verts[14], pane_verts[15]))
        bm.faces.new((pane_verts[13], pane_verts[12], pane_verts[8], pane_verts[9]))
        bm.faces.new((pane_verts[13], pane_verts[5], pane_verts[1], pane_verts[9]))
        bm.faces.new((pane_verts[13], pane_verts[12], pane_verts[14], pane_verts[15]))
        bm.faces.new((pane_verts[13], pane_verts[5], pane_verts[7], pane_verts[15])) 
        
        #door dependent faces
        if self.is_door:
            bm.faces.new((pane_verts[0], pane_verts[1], pane_verts[9], pane_verts[8]))
            bm.faces.new((pane_verts[2], pane_verts[3], pane_verts[11], pane_verts[10]))
        else:
            bm.faces.new((pane_verts[0], pane_verts[1], pane_verts[3], pane_verts[2]))
            bm.faces.new((pane_verts[0], pane_verts[2], pane_verts[10], pane_verts[8]))
            bm.faces.new((pane_verts[11], pane_verts[3], pane_verts[1], pane_verts[9]))
            bm.faces.new((pane_verts[11], pane_verts[9], pane_verts[8], pane_verts[10]))
            