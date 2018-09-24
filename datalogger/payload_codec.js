function Decode(fPort, bytes) {
    var decoded = {}
    if (fPort == 1) {
	decoded.year = (((bytes[0])))
	    decoded.month = (((bytes[1])))
	    decoded.day =  (((bytes[2])))
	    decoded.hours = (((bytes[3])))

	    decoded.minutes = (((bytes[4])))
	    decoded.seconds = (((bytes[5])))
	    decoded.degrees = (((bytes[6])))
	    decoded.fractional_degrees = (((bytes[7])))

	    return {"Year": decoded.year,
		    "Month": decoded.month,
		    "Day": decoded.day,
		    "Hours": decoded.hours,
		    "Minutes": decoded.minutes,
		    "Seconds": decoded.seconds,
		    "Degrees": decoded.degrees,
		    "Fractional_degrees": decoded.fractional_degrees
	};
    }
    return {};
}