// author Sheng Tang
// 09/05/2018  20:29

// find twitters that are post from 11pm to 6 am in workdays
// return the date and coordinate


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
		if(date[0]!='Fri'&&date[0]!='Sat'&&hour>13&&hour<=20){
			emit(date,doc.coordinates)
		}
	}
}
