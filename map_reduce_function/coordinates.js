// author Sheng Tang
// 09/05/2018  20:29

// return all twitters that have information about coordinates

function (doc) {
  var id,value;
  if (doc.id_str && doc.coordinates){
    id = doc.id_str;
    text = doc.text
    coordinates = doc.coordinates
    value = {"text":text,"coordinates":coordinates}
    emit(id,value)
  }
}