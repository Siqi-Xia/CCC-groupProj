function (doc) {
  var id,value;
  if (doc.id_str){
    id = doc.id_str;
    value = doc.text;
    emit(id,value);
  }
}