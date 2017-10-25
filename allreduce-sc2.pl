#!/usr/bin/perl

if (! defined $ARGV[0]) {
	print "\n Usage: allreduce.pl  <UT> <ObsId> <name> \n";
	print "\nut : ";
	chomp($ut = <STDIN>);
} else {
	$ut = $ARGV[0];
}
if (! defined $ARGV[1]) {
	print "ObsID : ";
	chomp($ObsID = <STDIN>);
} else {
	$ObsID = $ARGV[1];
}
if (! defined $ARGV[2]) {
	print "Name : ";
	chomp($Name = <STDIN>);
} else {
	$Name = $ARGV[2];
}
unlink "allfiles.list";
$padObsID = '0'x(5-length($ObsID)).$ObsID;


system("ls /jcmtdata/raw/scuba2/s8?/${ut}/${padObsID}/\* > allfiles.list");

$mmfile = "s850_${ut}\_${padObsID}\_${Name}_askbc";
$log = "s850_${ut}\_${padObsID}\_${Name}_askbc.log";

$mypara = "in=\\'^allfiles.list\\' out=\\'$mmfile\\' method=iterate config=\'\"^dimmconfig_askbc.lis\"\'";

print ">> makemap $mypara pixsize=3 |& tee $log \n";
system("$ENV{SMURF_DIR}/makemap $mypara pixsize=3 |& tee $log ");
#

