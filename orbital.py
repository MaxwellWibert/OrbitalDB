def parse_float(s):
    return float(s[0] + '.' + s[1:6] + 'e' + s[6:8])
def parse_dec(s):
    return float('.' + s)
class TLE:
    #dictionary for passing in default arguments to kwargs for __init__ method.
    default_params = {
        name: "", 
        sat_num : 0,
        classification: "U",
        id_year: 0,
        id_launch: 0,
        id_piece: A,
        epoch_year: 0,
        epoch: 0,
        mean_motion_p: 0,
        mean_motion_pp: 0,
        BSTAR: 0,
        element_num: 0,
        satellite_num: 0,
        inclination: 0,
        RAAD: 0,
        eccentricity: 0,
        arg_perigee: 0,
        mean_anomaly: 0,
        mean_motion: 0,
        rev_num: 0)
    }
    """ creates single TLE object, meant to represent a single observation of a satellite with relevant information about the time of observation,
    the satellite's origins and orbital characteristics"""
    __init__(self, *ignore,**kwargs = default_params)
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
        
        self.BSTAR = parse_float(self.BSTAR)

        self.element_num = int(self.element_num)

        self.inclination = float(self.inclination)
        self.RAAD = float(self.RAAD)
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
        return map(lambda bunch: cls.parse_tle(bunch),line_bunches)


    

    #takes: three lines: the name followed by the tle lines in string form
    #returns: TLE instance with params determined by tle lines
    @classmethod
    def parse_tle(cls, line0, line1, line2):
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
            BSTAR: line1[53:60],
            element_num: line1[64:67],
            #line 2 params
            inclination: line2[8:15],
            RAAD: line2[17:24],
            eccentricity: line2[26:32],
            arg_perigee: line2[34:41],
            mean_anomaly: line2[43:50],
            mean_motion: line2[52:62],
            rev_num: line2[63:67]
        }

        return TLE(params)

    
