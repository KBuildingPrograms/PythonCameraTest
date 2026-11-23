# Imports
if __name__ == '__main__' or __name__ == 'fpl_lib':
    import license_strings as lic
else:
    from ..libs import license_strings as lic

# Module metadata
__copyright__ = lic.copyright_str
__author__ = lic.author
__status__ = lic.status
__doc__ = "DESCRIPTION: Floating Point Library"

# FPL conversion functions
def parse_float(float_in, s, m, e):
    """
        Description:
        * Parse an input floating point signal into its encoded sign, mantissa and exponent components.
        * Encoded values: actual values STORED in memory.
        * Decoded values: actual REPRESENTED values.
        * Bit packing is: (MSB) s,e,e,e,e,m,m,m,m,m,m,m,m (LSB).
        * Bit length is s + e + m.
    """
    # Extract the components
    se = (float_in >> (e + m)) & ((1 << s) - 1)
    ee = (float_in >> m)       & ((1 << e) - 1)
    me =  float_in             & ((1 << m) - 1)

    # Done
    return se, me, ee

def combine_float(se, me, ee, s, m, e):
    """
        Description:
        * Combine an encoded mantissa, exponent and sign into a floating point signal.
        * Encoded values: actual values STORED in memory.
        * Decoded values: actual REPRESENTED values.
        * Bit packing is: (MSB) s,e,e,e,e,m,m,m,m,m,m,m,m (LSB).
        * Bit length is s + e + m.
    """
    # Combine the components
    float_out = ((se & ((1 << s) - 1)) << (e + m)) + \
                ((ee & ((1 << e) - 1)) << (m))     + \
                 (me & ((1 << m) - 1))
    # Done
    return float_out

def decode_float(se, me, ee, s, m, e):
    """
        Description:
        * Computes the decoded sign, exponent and mantissa from their
        * Encoded values: actual values STORED in memory.
        * Decoded values: actual REPRESENTED values.
        * Bit packing is: (MSB) s,e,e,e,e,m,m,m,m,m,m,m,m (LSB).
        * Bit length is s + e + m.
    """

    # Clip values
    se = se & ((1 << s) - 1)
    ee = ee & ((1 << e) - 1)
    me = me & ((1 << m) - 1)

    # Decode components
    if (ee == 0):
        # If encoded exponent is zero, then set decoded exponent to zero
        # and decoded mantissa to the encoded mantissa.
        md = me
        ed = 0
    else:
        # Add the leading MSB to the encoded mantissa.
        md = me + (1 << m)

        # Subtract one from the encoded mantissa
        ed = ee - 1
    #Encoded and decoded are the same
    sd = se

    # Done
    return sd, md, ed

def encode_float(sd, md, ed, s, m, e):
    """
        Description:
        * Computes the encoded sign, exponent and mantissa from their decoded counterparts.
        * Encoded values: actual values STORED in memory.
        * Decoded values: actual REPRESENTED values.
        * Bit packing is: (MSB) s,e,e,e,e,m,m,m,m,m,m,m,m (LSB).
        * Bit length is s + e + m.
    """
    # Encode components
    if (ed == 0):
        # If decoded exponent is zero, then set encoded exponent to zero
        # and encoded mantissa to the decoded mantissa.
        me = md
        ee = 0
    else:
        # Ignore the leading MSB from the decoded mantissa
        me = md & ((1 << m) - 1)

        # Add one to the decode mantissa
        ee = ed + 1

    # Encoded and decoded are the same
    se = sd

    # Clip values before output
    se = se & ((1 << s) - 1)
    ee = ee & ((1 << e) - 1)
    me = me & ((1 << m) - 1)

    # Done
    return se, me, ee

def find_nonzero_msb(inp, bitlength, min_pos):
    """
        Description: find the 1st non-zero MSB in an input
    """

    # Find the 1st non-zero MSB in an input

    # Reset the prev flag
    prev_msb_found = 0

    # Set the position of the non-zero msb to the minimum search position (defined as input)
    nonzero_msb = min_pos

    # Search at each bit position
    for bit_ind in range(bitlength - 1, min_pos, -1):
        # Shift the input and check if it is 1
        # Set the flag if true

        if (1 == ((inp >> bit_ind) & ((1 << 1) - 1))):
            msb_found = 1
        else:
            msb_found = 0

        # If the previous checked bit was zero and the current bit is 1,
        # then record the position
        if ((prev_msb_found == 0) and (msb_found == 1)):
            nonzero_msb = bit_ind

        # Set the previous flag to 1 only if the current or prev flags are true
        prev_msb_found = prev_msb_found or msb_found

    # Done
    return nonzero_msb

def fixed_to_float(fixed_in, s, m, e):
    """
        Description:
        * Convert a signed fixed point number into a floating point signal
        * Encoded values: actual values STORED in memory.
        * Decoded values: actual REPRESENTED values.
        * Bit packing is: (MSB) s,e,e,e,e,m,m,m,m,m,m,m,m (LSB).
        * Bit length is s + e + m.
    """

    # Determine the sign
    if (fixed_in < 0):
        se = 1
        fixed_in_abs = -1*fixed_in
    else:
        se = 0
        fixed_in_abs = fixed_in

    # Find the 1st nonzero MSB in the fixed value
    bitlength = m + (1 << e)
    min_value = m - 1
    nonzero_msb = find_nonzero_msb(fixed_in_abs, bitlength, min_value)

    # Compute the encoded values
    ed = nonzero_msb - (m - 1)
    if (ed == 0):
        me = fixed_in_abs
        ee = 0
    else:
        ee = ed
        if (ee > 1):
            me = ((fixed_in_abs >> (ee - 2)) + 1) >> 1
        else:
            me = fixed_in_abs

    if (me > (1 << (m + 1)) - 1):
        if (ee == ((1 << e) - 1)):
            me = (1 << m) - 1
        else:
            ee = ee + 1
            me = 0
    else:
        me = me & ((1 << m) - 1)

    # Combine the encoded values into a single bit value
    float_out = combine_float(se, me, ee, s, m, e)

    # Done
    return float_out

def float_to_fixed(float_in, s, m, e):
    """
        Description:
        * Convert a floating point signal to its represented fixed point value.
        * Encoded values: actual values STORED in memory.
        * Decoded values: actual REPRESENTED values.
        * Bit packing is: (MSB) s,e,e,e,e,m,m,m,m,m,m,m,m (LSB).
        * Bit length is s + e + m.
    """

    # Extract the encoded components
    se, me, ee = parse_float(float_in, s, m, e)

    # Decode the components
    sd, md, ed = decode_float(se, me, ee, s, m, e)

    # Construct the fixed number representation of the floating point signal
    fixed_out = md << ed
    if (sd == 1):
        fixed_out = -1*fixed_out

    # Done
    return fixed_out

def get_range(s, m, e):
    """
        Description: Absolute component extrema (encoded)
    """
    max_e = (1 << e) - 1
    max_m = (1 << m) - 1
    min_e = 0
    min_m = 0

    # Decode
    max_sd, max_md, max_ed = decode_float(0, max_m, max_e, 0, m, e)
    min_sd, min_md, min_ed = decode_float(0, min_m, min_e, 0, m, e)

    # Absolute value extrema
    min_abs = (min_md << min_ed)
    max_abs = (max_md << max_ed)

    # Signed extrema
    if (s == 1):
        min_p = min_abs
        max_p = max_abs
        min_n = -1*min_abs
        max_n = -1*max_abs
    else:
        min_p = min_abs
        max_p = max_abs
        min_n = -1*min_abs
        max_n = -1*max_abs

    # Done
    return min_p, max_p, min_n, max_n