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
        self.satellite_num = int(self.satellite_num)

        self.inclination = float(self.inclination)
        self.RAAD = float(self.RAAD)
        self.eccentricity = parse_dec(self.eccentricity)
        self.arg_perigee = float(self.arg_perigee)
        self.mean_anomaly = float(self.mean_anomaly)
        self.mean_motion = float(self.mean_motion)
        self.rev_num = int(self.rev_num)

        return self


    def generate_tles(path):
