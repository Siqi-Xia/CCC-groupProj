##author Sheng Tang
##09/05/2018  20:28


import pycouchdb
import couchdbProcesser as couchdbProcesser





############################################################################################################################
######  only create a view if there needs a new one or the map_reduce function have been updated      ######################
######              use query if you just want to get your data from an exist view !!!                ######################
############################################################################################################################



view_id = couchdbProcesser.create_view('db_twitters','id','','id_str')
view_id_count = couchdbProcesser.create_view('db_twitters','id','_count','id_str')


view_alcohol_related = couchdbProcesser.create_view('db_twitters','alcohol_related','','id_str')


view_coordinates= couchdbProcesser.create_view('db_twitters','coordinates','','id_str')


view_dateoftwitter_count = couchdbProcesser.create_view('db_twitters','dateoftwitter','_count','id_str')
view_stayuplateinworkday = couchdbProcesser.create_view('db_twitters','stayuplateinworkday','','id_str')
view_twitterinworkday = couchdbProcesser.create_view('db_twitters','twitterinworkday','','id_str')


