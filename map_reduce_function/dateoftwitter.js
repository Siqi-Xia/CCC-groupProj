// author Sheng Tang
// 09/05/2018  20:29


function (doc) {
	date=[]
	if (doc.id&&doc.created_at){
		time = doc.created_at
		t=time.split(' ')

		for (var i = 0; i <3; i++) {
				date.push(t[i])
			}
		emit(date,1)
	}
}
