// author Sheng Tang
// 09/05/2018  20:29

// use string match to find twitters that might relate to alcohol




function (doc) {
  var id,value
  if (alcohol_related(doc)&&doc.coordinates){
    id = doc.id_str
    value = {"text":doc.text,"coordinates":doc.coordinates}
    emit(id,value)
  }
}


function alcohol_related(doc) {
	related = false

	alcohol = ['alcohol', 'drink', 'cider', 'bbooze', 'beer', 'drunk',
                   'stoned', 'wasted', 'plastered', 'smashed', 'wrecked', 'high', 'beer',
                   'vodka', 'wine', 'alcoholic', 'champagne', 'hennessey', 'grey goose',
                   'truth serum', 'beverage', 'ale', 'liquor', 'liqueur', 'meaning of life',
                   'drinking', 'whiskey', 'spirits', 'malt', 'bar', 'bars', 'honkytonk',
                   'party', 'shitfaced', 'hangover', 'shit faced', 'tanked', 'sloshed',
                   'trashed', 'blackout', 'pissed',];


	text = doc.text.toLowerCase()
	twitter_word = text.split(" ")


  for (var i = twitter_word.length - 1; i >= 0; i--) {
    if(alcohol.indexOf(twitter_word[i]) !=-1){
      related = true
    }
  }

	return related;
}
