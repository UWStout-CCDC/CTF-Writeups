#!/usr/bin/perl
use strict;
use warnings;
use Digest::SHA qw(sha256_hex);

my $target_hash = "00ac7414402727fdf04c16b5dd7eb54533f459ff1943905e3e3143388e9460da";
my $start_time = 1734515700; # 21:55 CST
my $end_time = 1734516000;   # 22:00 CST


sub random_string {
    my ($seed, $length) = @_;
    srand($seed);
    my @chars = ('a'..'z', 'A'..'Z', '0'..'9');
    my $random_string = '';
    for (1..$length) {
        $random_string .= $chars[int(rand(@chars))];
    }
    return $random_string;
}

for my $seed ($start_time..$end_time) {
    my $random_str = random_string($seed, 16);
    my $flag = "STOUTCTF{" . $random_str . "}";

    my $hash = $flag;
    for (0..65) {
        $hash = sha256_hex($hash);
        if ($hash eq $target_hash) {
            print "$flag\n";
            last;
        }
    }


}
