import math
#physical/pathematical constants

MU = 3.986004418 * (10**14) #earth gravitational parameter
PI = math.pi #circle constant
#
R_E = 6378000 #radius of earth in meters

def parse_float(s):
    return float(s[0] + '.' + s[1:6] + 'e' + s[6:8])
def parse_dec(s):
    return float('.' + s)
class TLE:
    #dictionary for passing in default arguments to kwargs for __init__ method.

    """ creates single TLE object, meant to represent a single observation of a satellite with relevant information about the time of observation,
    the satellite's origins and orbital characteristics"""
    def __init__(self, *ignore,**kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

        #correcting data types and formatting below this line
        self.sat_num = int(self.sat_num)
        #reformats year
        self.id_year = int(self.id_year)
        if( self.id_year < 58 ):
            self.id_year += 2000
        else:
            self.id_year += 1900

        self.id_launch = int(self.id_launch)

        self.epoch_year = int(self.epoch_year)
        if( self.epoch_year < 58):
            self.epoch_year += 2000
        else:
            self.epoch_year += 1900
        self.epoch = float(self.epoch)

        self.mean_motion_p = float(self.mean_motion_p)
        self.mean_motion_pp = parse_float(mean_motion_pp)
        
        self.bstar = parse_float(self.bstar)

        self.element_num = int(self.element_num)

        self.inclination = float(self.inclination)
        self.raad = float(self.raad)
        self.eccentricity = parse_dec(self.eccentricity)
        self.arg_perigee = float(self.arg_perigee)
        self.mean_anomaly = float(self.mean_anomaly)
        self.mean_motion = float(self.mean_motion)
        self.rev_num = int(self.rev_num)

        return self

    #takes: path to TLE.txt file
    #returns: list of TLE instances with parameters matching specified by text file.
    @classmethod
    def parse_file(cls,path):
        with open(path, "r") as io:
            lines = io.readlines()
            io.close()
        line_bunches = [lines[i:i+2] for i in range(0, len(lines), 3)]
        return map(lambda bunch: cls.parse_tle(bunch[0], bunch[1], bunch[2]),line_bunches)


    

    #takes: three lines: the name followed by the tle lines in string form
    #returns: TLE instance with params determined by tle lines
    @classmethod
    def parse_tle(cls, line0, line1, line2):
        print('parsing:\n', line0, '\n', line1, '\n', line2)
        params = {
            #line 0 is just the name of the satellite
            name: line0,
            #line 1 params
            sat_num: line1[2:6],
            classification: line1[7],
            id_year: line1[9:10],
            id_launch: line1[11:12],
            id_piece: line1[14:16],
            epoch_year: line1[18:19],
            epoch: line1[20:31],
            mean_motion_p: line1[33:42],
            mean_motion_pp: line1[44:51],
            bstar: line1[53:60],
            element_num: line1[64:67],
            #line 2 params
            inclination: line2[8:15],
            raad: line2[17:24],
            eccentricity: line2[26:32],
            arg_perigee: line2[34:41],
            mean_anomaly: line2[43:50],
            mean_motion: line2[52:62], # in rotations per day
            rev_num: line2[63:67]
                }

        return TLE(params)
    
    #calculated parameters
    
    def period(self):  # length of time to revolve around earth once (in days)
        return 1/self.mean_motion
  
    def a(self):  # length of semi-major axis
        return math.pow(MU*(self.period()/(2*pi))**2,1/3)
    
    def r_peri(self):  # smallest (perigee) distance from center of earth
        return (1-self.eccentricity)*self.a()
    
    def r_apo(self):  # largest (apogee) distance from center of earth
        return (1 + self.eccentricity)*self.a()
    
    def h_peri(self):  # smallest (perigee) height from earth surface
        return self.r_peri() + R_E
    
    def h_apo(self):  # biggest (apogee) height from earthe surface
        return self.r_apo() + R_E
    
    def energy(self):
        return -MU/(2*self.a())
    
    def PE_peri(self):
        return -MU/self.r_peri()
    
    def PE_apo(self):
        return -MU/self.r_apo()
    
    def KE_peri(self):
        return self.energy() - self.PE_peri()
    def KE_apo(self):
        return self.energy() - self.PE_apo()
    
    def speed_peri(self):
        return math.sqrt(2*self.KE_peri())
    def speed_apo(self):
        return math.sqrt(2*self.KE_apo())

    #calculating approximate true_anomaly from fourier expansion over mean anomaly with O(e^4) error
    def true_anomaly(self):
        MA = self.mean_anomaly
        E = self.eccentricity

        return (ma + (2*E -(E**3)/4)*math.sin(ma) + (5/4)*(E**2)*math.sin(2*ma) + (13/12)*(E**3)*math.sin(3*ma))

    #current distance from center of earth
    def radius(self): 
        e = self.eccentricity
        a = self.a()
        n = self.true_anomaly()

        return a * (1 - e**2)/(1+ e*math.cos(n))
    
    def height(self):
        return self.radius() - R_E
    

#class ends here
line0 = "IRIDIUM 33"
line1 = "1 24946U 97051C 20051.53657729 .00000083 00000-0 22736-4 0 9994" 
line2 = "2 24946 86.3857 237.2037 0006065 304.3927 55.6695 14.33674051174195"
TLE.parse_tle(line0,line1, line2)
