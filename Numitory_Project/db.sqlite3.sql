START TRANSACTION ;;
CREATE TABLE IF NOT EXISTS 'inventory_type' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'type_name'	varchar(100) NOT NULL UNIQUE,
	'type_desc'	varchar(250) NOT NULL,
	'user_id'	integer NOT NULL,
	'created'	datetime NOT NULL,
	'recycled'	boolean NOT NULL,
	FOREIGN KEY('user_id') REFERENCES 'auth_user'('id') 
);
CREATE TABLE IF NOT EXISTS 'inventory_item' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'item_name'	varchar(100) NOT NULL,
	'item_desc'	varchar(250) NOT NULL,
	'collection_id'	integer NOT NULL,
	'type_id'	integer NOT NULL,
	'user_id'	integer NOT NULL,
	'created'	datetime NOT NULL,
	'sold'	boolean NOT NULL,
	FOREIGN KEY('collection_id') REFERENCES 'inventory_collection'('id') ,
	FOREIGN KEY('type_id') REFERENCES 'inventory_type'('id') ,
	FOREIGN KEY('user_id') REFERENCES 'auth_user'('id') 
);
CREATE TABLE IF NOT EXISTS 'inventory_collection' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'coll_name'	varchar(100) NOT NULL UNIQUE,
	'coll_desc'	varchar(250) NOT NULL,
	'user_id'	integer NOT NULL,
	'created'	datetime NOT NULL,
	'recycled'	boolean NOT NULL,
	FOREIGN KEY('user_id') REFERENCES 'auth_user'('id') 
);
CREATE TABLE IF NOT EXISTS 'django_session' (
	'session_key'	varchar(40) NOT NULL,
	'session_data'	text NOT NULL,
	'expire_date'	datetime NOT NULL,
	PRIMARY KEY('session_key')
);
CREATE TABLE IF NOT EXISTS 'auth_user' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'password'	varchar(128) NOT NULL,
	'last_login'	datetime,
	'is_superuser'	boolean NOT NULL,
	'username'	varchar(150) NOT NULL UNIQUE,
	'last_name'	varchar(150) NOT NULL,
	'email'	varchar(254) NOT NULL,
	'is_staff'	boolean NOT NULL,
	'is_active'	boolean NOT NULL,
	'date_joined'	datetime NOT NULL,
	'first_name'	varchar(150) NOT NULL
);
CREATE TABLE IF NOT EXISTS 'auth_group' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'name'	varchar(150) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS 'auth_permission' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'content_type_id'	integer NOT NULL,
	'codename'	varchar(100) NOT NULL,
	'name'	varchar(255) NOT NULL,
	FOREIGN KEY('content_type_id') REFERENCES 'django_content_type'('id') 
);
CREATE TABLE IF NOT EXISTS 'django_content_type' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'app_label'	varchar(100) NOT NULL,
	'model'	varchar(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS 'django_admin_log' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'action_time'	datetime NOT NULL,
	'object_id'	text,
	'object_repr'	varchar(200) NOT NULL,
	'change_message'	text NOT NULL,
	'content_type_id'	integer,
	'user_id'	integer NOT NULL,
	'action_flag'	smallint unsigned NOT NULL CHECK('action_flag'>=0),
	FOREIGN KEY('content_type_id') REFERENCES 'django_content_type'('id') ,
	FOREIGN KEY('user_id') REFERENCES 'auth_user'('id') 
);
CREATE TABLE IF NOT EXISTS 'auth_user_user_permissions' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'user_id'	integer NOT NULL,
	'permission_id'	integer NOT NULL,
	FOREIGN KEY('user_id') REFERENCES 'auth_user'('id') ,
	FOREIGN KEY('permission_id') REFERENCES 'auth_permission'('id') 
);
CREATE TABLE IF NOT EXISTS 'auth_user_groups' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'user_id'	integer NOT NULL,
	'group_id'	integer NOT NULL,
	FOREIGN KEY('user_id') REFERENCES 'auth_user'('id') ,
	FOREIGN KEY('group_id') REFERENCES 'auth_group'('id') 
);
CREATE TABLE IF NOT EXISTS 'auth_group_permissions' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'group_id'	integer NOT NULL,
	'permission_id'	integer NOT NULL,
	FOREIGN KEY('group_id') REFERENCES 'auth_group'('id') ,
	FOREIGN KEY('permission_id') REFERENCES 'auth_permission'('id') 
);
CREATE TABLE IF NOT EXISTS 'django_migrations' (
	'id'	integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
	'app'	varchar(255) NOT NULL,
	'name'	varchar(255) NOT NULL,
	'applied'	datetime NOT NULL
);
INSERT IGNORE INTO 'inventory_type' VALUES (1,'New Type 11','Types are great and informative.',1,'2020-12-26 03:42:37.996900',0);
INSERT IGNORE INTO 'inventory_type' VALUES (2,'Type 2','Something About it Here',1,'2020-12-26 14:47:12.217291',0);
INSERT IGNORE INTO 'inventory_type' VALUES (3,'New Form Type','Something Here',1,'2020-12-26 15:59:20.363521',0);
INSERT IGNORE INTO 'inventory_type' VALUES (5,'New Type','Something',1,'2020-12-26 16:12:17.517657',0);
INSERT IGNORE INTO 'inventory_type' VALUES (6,'Type 3','Something Here',1,'2020-12-26 17:06:28.628102',0);
INSERT IGNORE INTO 'inventory_type' VALUES (7,'asdasfadfdf','sdfsdf',1,'2020-12-26 17:42:53.261529',0);
INSERT IGNORE INTO 'inventory_type' VALUES (8,'qewqe','qwe',1,'2020-12-26 17:43:27.643550',0);
INSERT IGNORE INTO 'inventory_type' VALUES (9,'New Type 2','Something',1,'2020-12-26 17:53:37.534171',0);
INSERT IGNORE INTO 'inventory_type' VALUES (10,'Confused','Yes I am',1,'2020-12-27 01:23:37.359207',0);
INSERT IGNORE INTO 'inventory_item' VALUES (1,'New Item','something',2,1,1,'2020-12-26 03:42:37.981572',0);
INSERT IGNORE INTO 'inventory_item' VALUES (2,'New Item','something',2,2,1,'2020-12-26 15:41:00.563176',0);
INSERT IGNORE INTO 'inventory_item' VALUES (3,'Simpler Item','Something',1,2,1,'2020-12-26 15:41:43.411165',0);
INSERT IGNORE INTO 'inventory_item' VALUES (4,'Yes!','Here and here',1,3,20,'2020-12-26 15:59:34.146534',0);
INSERT IGNORE INTO 'inventory_item' VALUES (5,'New Yes Something','This is great',3,2,1,'2020-12-26 17:33:39.367547',0);
INSERT IGNORE INTO 'inventory_item' VALUES (6,'New Item Fize','Something Here',3,3,1,'2020-12-26 17:34:36.407369',0);
INSERT IGNORE INTO 'inventory_item' VALUES (7,'add','asd',1,1,1,'2020-12-26 17:37:16.861295',0);
INSERT IGNORE INTO 'inventory_item' VALUES (8,'add','asd',1,1,1,'2020-12-26 17:37:39.917732',0);
INSERT IGNORE INTO 'inventory_item' VALUES (9,'Test Form Itesm','asd',1,1,1,'2020-12-26 17:38:26.472939',0);
INSERT IGNORE INTO 'inventory_item' VALUES (10,'asdasdsa','asd',1,1,1,'2020-12-26 17:39:10.700267',0);
INSERT IGNORE INTO 'inventory_item' VALUES (11,'asdasdsasad','ad',1,1,1,'2020-12-26 17:39:30.394824',0);
INSERT IGNORE INTO 'inventory_item' VALUES (12,'asdsadasd','asd',2,1,1,'2020-12-26 17:40:18.366498',0);
INSERT IGNORE INTO 'inventory_item' VALUES (13,'Redirect','Something',4,3,20,'2020-12-26 17:44:08.362257',0);
INSERT IGNORE INTO 'inventory_item' VALUES (14,'Footer Item','GRow',2,2,1,'2020-12-27 02:45:02.505990',0);
INSERT IGNORE INTO 'inventory_item' VALUES (15,'asdasdsaad','asd',1,2,1,'2020-12-27 02:45:15.566758',0);
INSERT IGNORE INTO 'inventory_item' VALUES (16,'aq','wq',1,1,1,'2020-12-27 03:03:46.890797',0);
INSERT IGNORE INTO 'inventory_item' VALUES (17,'qwwqe','qwe',1,2,1,'2020-12-27 03:03:56.344848',0);
INSERT IGNORE INTO 'inventory_item' VALUES (18,'2e21','12e',2,6,1,'2020-12-27 03:04:05.669485',0);
INSERT IGNORE INTO 'inventory_item' VALUES (19,'2e12e12','2e1',2,1,1,'2020-12-27 03:04:14.863479',0);
INSERT IGNORE INTO 'inventory_collection' VALUES (1,'Admin UPD2 Collection','This is the first one...',1,'2020-12-26 03:42:37.958738',0);
INSERT IGNORE INTO 'inventory_collection' VALUES (2,'Second 2 Collection','This is good.',1,'2020-12-26 14:48:36.042701',0);
INSERT IGNORE INTO 'inventory_collection' VALUES (3,'Third Collection','Somethin Good.',1,'2020-12-26 14:50:51.125801',0);
INSERT IGNORE INTO 'inventory_collection' VALUES (4,'New Form Coll','Something',1,'2020-12-26 15:56:25.541425',0);
INSERT IGNORE INTO 'inventory_collection' VALUES (5,'Something Coll','as',1,'2020-12-26 16:42:09.240537',0);
INSERT IGNORE INTO 'inventory_collection' VALUES (6,'Something Colls','sd',1,'2020-12-26 16:46:09.671765',0);
INSERT IGNORE INTO 'inventory_collection' VALUES (7,'Something Coll1','as',1,'2020-12-26 17:13:10.251440',0);
INSERT IGNORE INTO 'inventory_collection' VALUES (8,'adaa','asf',1,'2020-12-26 17:39:54.017762',0);
INSERT IGNORE INTO 'inventory_collection' VALUES (9,'Hot Collection','Something',1,'2020-12-26 17:54:01.980264',0);
INSERT IGNORE INTO 'inventory_collection' VALUES (10,'Test Shorten','Something',1,'2020-12-27 02:37:34.167955',0);
INSERT IGNORE INTO 'django_session' VALUES ('rpcfuqqbrzdso5pat7se8ls99ilwusu2','e30:1ksyp4:ycgXPsQTJ1aEKJmpIulOJwznwmYeslquNFu_D8a0F7c','2021-01-09 01:56:46.416676');
INSERT IGNORE INTO 'django_session' VALUES ('n4njw878pv3tb4shk1axnhcfkcuek6oj','.eJxVjMsOwiAQRf-FtSE8HKAu3fcbyAxMpWogKe3K-O_apAvd3nPOfYmI21ri1nmJcxYXoYM4_Y6E6cF1J_mO9dZkanVdZpK7Ig_a5dgyP6-H-3dQsJdvHch7CuqMDngKQStAtN6YpMAgGALDljRpROeIzQBKwUSsB6sTJZvF-wP3XDfl:1kszUK:Y9COXpxZtvScmI2f5cUtIWOE62VWiFkgjxs-tLSNnmI','2021-01-09 02:39:24.508390');
INSERT IGNORE INTO 'django_session' VALUES ('wdy4ixec56ni8sev6mrokk2immw06alt','.eJxVjMsOwiAQRf-FtSEw8nTp3m8gAwxSNZCUdmX8d9ukC92ec-59s4DrUsM6aA5TZhcm2emXRUxParvID2z3zlNvyzxFvif8sIPfeqbX9Wj_DiqOuq2tg1x8PBeZQWGSGYm8Nk4ZjAQikrZCaSml8IbAUQGtQQv0foPeGvb5AuZMNxY:1ktCr3:QMYsDDP02XFOqeajcr-XAOH6dptcPhbVfbngSdz8VqM','2021-01-09 16:55:45.988261');
INSERT IGNORE INTO 'auth_user' VALUES (1,'pbkdf2_sha256$216000$ubY9wxvxYgbx$KsSUjX9rZb6w73gbDV4O/iEXJ/yjqrXy/XQYN2FLunM=','2020-12-26 16:55:45.961332',1,'admin','','',1,1,'2020-12-26 00:55:42.197509','');
INSERT IGNORE INTO 'auth_user' VALUES (20,'pbkdf2_sha256$216000$sBeOWemR9UEu$yQ41mEF6KPuLhXUjmr1vFK2jfTnAcsmTLTrt4gMrGy0=','2020-12-26 11:27:22.824573',0,'as','','',0,1,'2020-12-26 11:27:22.382301','');
INSERT IGNORE INTO 'auth_permission' VALUES (1,1,'add_logentry','Can add log entry');
INSERT IGNORE INTO 'auth_permission' VALUES (2,1,'change_logentry','Can change log entry');
INSERT IGNORE INTO 'auth_permission' VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT IGNORE INTO 'auth_permission' VALUES (4,1,'view_logentry','Can view log entry');
INSERT IGNORE INTO 'auth_permission' VALUES (5,2,'add_permission','Can add permission');
INSERT IGNORE INTO 'auth_permission' VALUES (6,2,'change_permission','Can change permission');
INSERT IGNORE INTO 'auth_permission' VALUES (7,2,'delete_permission','Can delete permission');
INSERT IGNORE INTO 'auth_permission' VALUES (8,2,'view_permission','Can view permission');
INSERT IGNORE INTO 'auth_permission' VALUES (9,3,'add_group','Can add group');
INSERT IGNORE INTO 'auth_permission' VALUES (10,3,'change_group','Can change group');
INSERT IGNORE INTO 'auth_permission' VALUES (11,3,'delete_group','Can delete group');
INSERT IGNORE INTO 'auth_permission' VALUES (12,3,'view_group','Can view group');
INSERT IGNORE INTO 'auth_permission' VALUES (13,4,'add_user','Can add user');
INSERT IGNORE INTO 'auth_permission' VALUES (14,4,'change_user','Can change user');
INSERT IGNORE INTO 'auth_permission' VALUES (15,4,'delete_user','Can delete user');
INSERT IGNORE INTO 'auth_permission' VALUES (16,4,'view_user','Can view user');
INSERT IGNORE INTO 'auth_permission' VALUES (17,5,'add_contenttype','Can add content type');
INSERT IGNORE INTO 'auth_permission' VALUES (18,5,'change_contenttype','Can change content type');
INSERT IGNORE INTO 'auth_permission' VALUES (19,5,'delete_contenttype','Can delete content type');
INSERT IGNORE INTO 'auth_permission' VALUES (20,5,'view_contenttype','Can view content type');
INSERT IGNORE INTO 'auth_permission' VALUES (21,6,'add_session','Can add session');
INSERT IGNORE INTO 'auth_permission' VALUES (22,6,'change_session','Can change session');
INSERT IGNORE INTO 'auth_permission' VALUES (23,6,'delete_session','Can delete session');
INSERT IGNORE INTO 'auth_permission' VALUES (24,6,'view_session','Can view session');
INSERT IGNORE INTO 'auth_permission' VALUES (25,7,'add_collection','Can add collection');
INSERT IGNORE INTO 'auth_permission' VALUES (26,7,'change_collection','Can change collection');
INSERT IGNORE INTO 'auth_permission' VALUES (27,7,'delete_collection','Can delete collection');
INSERT IGNORE INTO 'auth_permission' VALUES (28,7,'view_collection','Can view collection');
INSERT IGNORE INTO 'auth_permission' VALUES (29,8,'add_type','Can add type');
INSERT IGNORE INTO 'auth_permission' VALUES (30,8,'change_type','Can change type');
INSERT IGNORE INTO 'auth_permission' VALUES (31,8,'delete_type','Can delete type');
INSERT IGNORE INTO 'auth_permission' VALUES (32,8,'view_type','Can view type');
INSERT IGNORE INTO 'auth_permission' VALUES (33,9,'add_item','Can add item');
INSERT IGNORE INTO 'auth_permission' VALUES (34,9,'change_item','Can change item');
INSERT IGNORE INTO 'auth_permission' VALUES (35,9,'delete_item','Can delete item');
INSERT IGNORE INTO 'auth_permission' VALUES (36,9,'view_item','Can view item');
INSERT IGNORE INTO 'django_content_type' VALUES (1,'admin','logentry');
INSERT IGNORE INTO 'django_content_type' VALUES (2,'auth','permission');
INSERT IGNORE INTO 'django_content_type' VALUES (3,'auth','group');
INSERT IGNORE INTO 'django_content_type' VALUES (4,'auth','user');
INSERT IGNORE INTO 'django_content_type' VALUES (5,'contenttypes','contenttype');
INSERT IGNORE INTO 'django_content_type' VALUES (6,'sessions','session');
INSERT IGNORE INTO 'django_content_type' VALUES (7,'inventory','collection');
INSERT IGNORE INTO 'django_content_type' VALUES (8,'inventory','type');
INSERT IGNORE INTO 'django_content_type' VALUES (9,'inventory','item');
INSERT IGNORE INTO 'django_admin_log' VALUES (1,'2020-12-26 03:30:46.918345','9','asd','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (2,'2020-12-26 03:30:46.957639','11','asdd','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (3,'2020-12-26 03:30:46.977753','14','asddd','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (4,'2020-12-26 03:30:47.009912','12','asdj','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (5,'2020-12-26 03:30:47.032521','2','asdsd','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (6,'2020-12-26 03:30:47.059020','16','ass','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (7,'2020-12-26 03:30:47.082101','19','assss','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (8,'2020-12-26 03:30:47.108197','15','bob_joe','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (9,'2020-12-26 03:30:47.137381','18','br','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (10,'2020-12-26 03:30:47.186398','10','lkj','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (11,'2020-12-26 03:30:47.216291','17','markd','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (12,'2020-12-26 03:30:47.240490','13','matt','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (13,'2020-12-26 03:30:47.261523','3','mike','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (14,'2020-12-26 03:30:47.298194','4','mike2','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (15,'2020-12-26 03:30:47.337167','5','mike3','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (16,'2020-12-26 03:30:47.359364','8','mikem','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (17,'2020-12-26 03:30:47.376575','7','mikemck','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (18,'2020-12-26 03:30:47.387107','6','mikepmck','',4,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (19,'2020-12-26 03:31:30.406580','1','Collection object (1)','[{'added': {}}]',7,1,1);
INSERT IGNORE INTO 'django_admin_log' VALUES (20,'2020-12-26 03:32:04.031445','1','Type object (1)','[{'added': {}}]',8,1,1);
INSERT IGNORE INTO 'django_admin_log' VALUES (21,'2020-12-26 03:32:15.308252','1','Item object (1)','[{'added': {}}]',9,1,1);
INSERT IGNORE INTO 'django_admin_log' VALUES (22,'2020-12-26 03:44:14.399324','1','New Type 1 ->  Types are great and informative.','[{'changed': {'fields': ['Type desc']}}]',8,1,2);
INSERT IGNORE INTO 'django_admin_log' VALUES (23,'2020-12-26 14:47:12.220653','2','Type 2 ->  Something About it Here','[{'added': {}}]',8,1,1);
INSERT IGNORE INTO 'django_admin_log' VALUES (24,'2020-12-26 14:48:36.044624','2','Second Collection ->  This is good.','[{'added': {}}]',7,1,1);
INSERT IGNORE INTO 'django_admin_log' VALUES (25,'2020-12-26 14:50:51.129952','3','Third Collection ->  Somethin Good.','[{'added': {}}]',7,1,1);
INSERT IGNORE INTO 'django_admin_log' VALUES (26,'2020-12-26 16:48:28.396241','4','New Type','',8,1,3);
INSERT IGNORE INTO 'django_admin_log' VALUES (27,'2020-12-26 17:25:52.221886','4','Yes! ->  Here and here','[{'changed': {'fields': ['User']}}]',9,1,2);
INSERT IGNORE INTO 'django_admin_log' VALUES (28,'2020-12-26 19:53:15.970903','9','New Type 2','[{'changed': {'fields': ['Recycled']}}]',8,1,2);
INSERT IGNORE INTO 'django_admin_log' VALUES (29,'2020-12-26 19:57:58.493186','9','New Type 2','[{'changed': {'fields': ['Recycled']}}]',8,1,2);
INSERT IGNORE INTO 'django_admin_log' VALUES (30,'2020-12-26 19:58:06.795869','13','Redirect ->  Something','[{'changed': {'fields': ['Recycled']}}]',9,1,2);
INSERT IGNORE INTO 'django_admin_log' VALUES (31,'2020-12-26 19:58:48.750384','13','Redirect ->  Something','[{'changed': {'fields': ['Recycled']}}]',9,1,2);
INSERT IGNORE INTO 'django_admin_log' VALUES (32,'2020-12-26 23:44:56.135073','13','Redirect ->  Something','[{'changed': {'fields': ['User']}}]',9,1,2);
INSERT IGNORE INTO 'django_migrations' VALUES (1,'contenttypes','0001_initial','2020-12-25 22:45:52.962845');
INSERT IGNORE INTO 'django_migrations' VALUES (2,'auth','0001_initial','2020-12-25 22:45:52.996046');
INSERT IGNORE INTO 'django_migrations' VALUES (3,'admin','0001_initial','2020-12-25 22:45:53.040922');
INSERT IGNORE INTO 'django_migrations' VALUES (4,'admin','0002_logentry_remove_auto_add','2020-12-25 22:45:53.066970');
INSERT IGNORE INTO 'django_migrations' VALUES (5,'admin','0003_logentry_add_action_flag_choices','2020-12-25 22:45:53.091926');
INSERT IGNORE INTO 'django_migrations' VALUES (6,'contenttypes','0002_remove_content_type_name','2020-12-25 22:45:53.127830');
INSERT IGNORE INTO 'django_migrations' VALUES (7,'auth','0002_alter_permission_name_max_length','2020-12-25 22:45:53.155299');
INSERT IGNORE INTO 'django_migrations' VALUES (8,'auth','0003_alter_user_email_max_length','2020-12-25 22:45:53.185407');
INSERT IGNORE INTO 'django_migrations' VALUES (9,'auth','0004_alter_user_username_opts','2020-12-25 22:45:53.217251');
INSERT IGNORE INTO 'django_migrations' VALUES (10,'auth','0005_alter_user_last_login_null','2020-12-25 22:45:53.241182');
INSERT IGNORE INTO 'django_migrations' VALUES (11,'auth','0006_require_contenttypes_0002','2020-12-25 22:45:53.256143');
INSERT IGNORE INTO 'django_migrations' VALUES (12,'auth','0007_alter_validators_add_error_messages','2020-12-25 22:45:53.288058');
INSERT IGNORE INTO 'django_migrations' VALUES (13,'auth','0008_alter_user_username_max_length','2020-12-25 22:45:53.319973');
INSERT IGNORE INTO 'django_migrations' VALUES (14,'auth','0009_alter_user_last_name_max_length','2020-12-25 22:45:53.341935');
INSERT IGNORE INTO 'django_migrations' VALUES (15,'auth','0010_alter_group_name_max_length','2020-12-25 22:45:53.367682');
INSERT IGNORE INTO 'django_migrations' VALUES (16,'auth','0011_update_proxy_permissions','2020-12-25 22:45:53.399869');
INSERT IGNORE INTO 'django_migrations' VALUES (17,'auth','0012_alter_user_first_name_max_length','2020-12-25 22:45:53.434316');
INSERT IGNORE INTO 'django_migrations' VALUES (18,'inventory','0001_initial','2020-12-25 22:45:53.466860');
INSERT IGNORE INTO 'django_migrations' VALUES (19,'sessions','0001_initial','2020-12-25 22:45:53.485896');
INSERT IGNORE INTO 'django_migrations' VALUES (20,'inventory','0002_auto_20201225_2029','2020-12-26 03:29:50.949213');
INSERT IGNORE INTO 'django_migrations' VALUES (21,'inventory','0003_auto_20201225_2042','2020-12-26 03:42:38.001588');
INSERT IGNORE INTO 'django_migrations' VALUES (22,'inventory','0004_auto_20201226_0933','2020-12-26 16:48:43.263108');
INSERT IGNORE INTO 'django_migrations' VALUES (23,'inventory','0005_auto_20201226_1253','2020-12-26 19:53:04.772929');
INSERT IGNORE INTO 'django_migrations' VALUES (24,'inventory','0006_auto_20201226_1655','2020-12-26 23:55:09.529732');
CREATE INDEX IF NOT EXISTS 'inventory_type_user_id_5e7955f4' ON 'inventory_type' (
	'user_id'
);
CREATE INDEX IF NOT EXISTS 'inventory_item_user_id_f563f0c1' ON 'inventory_item' (
	'user_id'
);
CREATE INDEX IF NOT EXISTS 'inventory_item_type_id_169bec09' ON 'inventory_item' (
	'type_id'
);
CREATE INDEX IF NOT EXISTS 'inventory_item_collection_id_2ec35ddc' ON 'inventory_item' (
	'collection_id'
);
CREATE INDEX IF NOT EXISTS 'inventory_collection_user_id_5ae91810' ON 'inventory_collection' (
	'user_id'
);
CREATE INDEX IF NOT EXISTS 'django_session_expire_date_a5c62663' ON 'django_session' (
	'expire_date'
);
CREATE INDEX IF NOT EXISTS 'auth_permission_content_type_id_2f476e4b' ON 'auth_permission' (
	'content_type_id'
);
CREATE UNIQUE INDEX IF NOT EXISTS 'auth_permission_content_type_id_codename_01ab375a_uniq' ON 'auth_permission' (
	'content_type_id',
	'codename'
);
CREATE UNIQUE INDEX IF NOT EXISTS 'django_content_type_app_label_model_76bd3d3b_uniq' ON 'django_content_type' (
	'app_label',
	'model'
);
CREATE INDEX IF NOT EXISTS 'django_admin_log_user_id_c564eba6' ON 'django_admin_log' (
	'user_id'
);
CREATE INDEX IF NOT EXISTS 'django_admin_log_content_type_id_c4bce8eb' ON 'django_admin_log' (
	'content_type_id'
);
CREATE INDEX IF NOT EXISTS 'auth_user_user_permissions_permission_id_1fbb5f2c' ON 'auth_user_user_permissions' (
	'permission_id'
);
CREATE INDEX IF NOT EXISTS 'auth_user_user_permissions_user_id_a95ead1b' ON 'auth_user_user_permissions' (
	'user_id'
);
CREATE UNIQUE INDEX IF NOT EXISTS 'auth_user_user_permissions_user_id_permission_id_14a6b632_uniq' ON 'auth_user_user_permissions' (
	'user_id',
	'permission_id'
);
CREATE INDEX IF NOT EXISTS 'auth_user_groups_group_id_97559544' ON 'auth_user_groups' (
	'group_id'
);
CREATE INDEX IF NOT EXISTS 'auth_user_groups_user_id_6a12ed8b' ON 'auth_user_groups' (
	'user_id'
);
CREATE UNIQUE INDEX IF NOT EXISTS 'auth_user_groups_user_id_group_id_94350c0c_uniq' ON 'auth_user_groups' (
	'user_id',
	'group_id'
);
CREATE INDEX IF NOT EXISTS 'auth_group_permissions_permission_id_84c5c92e' ON 'auth_group_permissions' (
	'permission_id'
);
CREATE INDEX IF NOT EXISTS 'auth_group_permissions_group_id_b120cbf9' ON 'auth_group_permissions' (
	'group_id'
);
CREATE UNIQUE INDEX IF NOT EXISTS 'auth_group_permissions_group_id_permission_id_0cd325b0_uniq' ON 'auth_group_permissions' (
	'group_id',
	'permission_id'
);
;;
