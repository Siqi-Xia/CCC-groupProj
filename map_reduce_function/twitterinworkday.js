// author Sheng Tang
// 09/05/2018  20:29

// find all twitters that are post in workday
// return data and coordinates


function (doc) {
	date=[]
	if (doc.id&&doc.created_at&&doc.coordinates){
		time = doc.created_at
		t=time.split(' ')

		for (var i = 0; i <3; i++) {
				date.push(t[i])
			}
		hour=parseInt(t[3].split(":")[0])


		//transfer from GMT TO MEL local time	
		if(date[0]!='Fri'&&date[0]!='Sat'){
			emit(date,doc.coordinates)
		}
	}
}