# curator-for-aws-es-domain

Work's with AWS ES domain 5.1

Remember that the line 90 in curator.py is commented.
If you want to delete indexes remove the comment!

### Install
`$> pip install requests`

### Configuration
You can set a new retention value for the one specific index by modifying the file curator_retention_conf.csv.

Just follow the example:

`[index-prefix1]:[retention_day]`

### Launch
`$> ./curator.py search-[es-name]-[es-hash].[es-region].es.amazonaws.com`


### Credits

* **Dorian 'warp' COLNOT**
* [All contributors](https://github.com/w4rppy/curator-for-aws-es-domain/graphs/contributors)
