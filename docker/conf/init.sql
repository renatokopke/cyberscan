USE scan;

CREATE TABLE IF NOT EXISTS `teste` (
  `id` int(11) NOT NULL auto_increment,
  `recid` int(11) NOT NULL default '0',
  `cvfilename` varchar(250)  NOT NULL default '',
  `cvpagenumber`  int(11) NULL,
  `cilineno` int(11)  NULL,
  `batchname`  varchar(100) NOT NULL default '',
  `type` varchar(20) NOT NULL default '',
  `data` varchar(100) NOT NULL default '',
   PRIMARY KEY  (`id`)
);