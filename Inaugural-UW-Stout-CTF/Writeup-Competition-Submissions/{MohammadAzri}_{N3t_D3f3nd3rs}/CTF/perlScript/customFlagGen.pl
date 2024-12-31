#!/usr/bin/perl
use strict;
use warnings;

# Welcome message
print "Generating a super random CTF flag";

# Get the current time as a seed
my $seed = time;

# Seed the random number generator
srand($seed);

# Define a function to generate a super dupper advanced and secure random string
sub random_string {
    my ($length) = @_;
    my @chars = ('a'..'z', 'A'..'Z', '0'..'9');
    my $random_string = '';
    
    for (1..$length) {
        $random_string .= $chars[int(rand(@chars))];
    }
    
    return $random_string;
}

# Generate the flag
my $flag = "STOUTCTF{" . random_string(16) . "}";

# Print the generated flag
print "Generated Flag: $flag\n";
