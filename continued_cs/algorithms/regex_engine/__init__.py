'''
This is basically just a cleaned-up version of this solution:

    http://jianlu.github.io/2016/11/07/leetcode10-Regular-Expression-Matching/

My goal was to understand what's going on because all the indices and the slight indexing difference
between M and text / pattern was confusing me.
'''
import logging


LOG_FORMAT = '%(levelname)s:%(filename)s:%(funcName)s:%(lineno)s - %(message)s'
LOG_STATE_MSG = "  State for t={} p={}:: {}"
LOG_RESULT_MSG = "  result for t={} p={}: {}"
DEBUG_VARS = ('two_fewer_p_worked_same_t',
              'one_fewer_p_worked_same_t',
              'prev_p_was_dot_or_matched_this_t',
              'same_pattern_one_fewer_t_was_success')

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def is_match(text, pattern):
    return IsMatch(text, pattern).is_match()


class IsMatch(object):
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern

        # Create the matrix that will hold our partial solutions. M[t][p] is a boolean value
        # indicating the result of:
        #
        #    is_match(text[:t-1], pattern[:p-1])
        #
        # Why are the row / columns indices t and p but the text indices are t-1 and p-1? Because
        # we need to account for empty texts and patterns. Thus, M[t][p] really means "the solution
        # for t characters in text and p characters in pattern". Since Python is 0-indexed, that
        # accounts for the discrepancy.
        self.max_t = len(self.text)
        self.max_p = len(self.pattern)
        self.M = [[False for p in range(self.max_p+1)] for t in range(self.max_t+1)]

    def pchar_at_M_idx(self, p):
        '''
        This and tchar_at_M_idx are trivial methods, but I have a lot of trouble following this
        solution given that M[t][p] actually means "the partial solution at text index t-1 and at
        pattern index p-1 instead of at indices t and p.
        '''
        return self.pattern[p-1]

    def tchar_at_M_idx(self, t):
        return self.text[t-1]

    def is_match(self):
        # An empty text matches an empty pattern
        self.M[0][0] = True

        # Initialize M[0][p] for p = 2,...,max_p
        # If the 2nd character in the pattern is a *, then one option would be to just negate it and
        # the previous pattern character, i.e. we could match the pattern part 'a*' to zero
        # characters in text. Here we do that to initialize that set of possibilities when our text
        # is length 0, i.e. we make sure pattern 'a*b*c*' would all equal text ''. We do this by
        # saying that if the solution with 2 fewer pattern characters works, then this works as well
        for p in range(2, self.max_p+1):
            if self.pchar_at_M_idx(p) == '*':
                self.M[0][p] = self.M[0][p-2]

        # We now iterate through all characters in our text (remember that 1 here means the 1st
        # character in `text` and NOT the 2nd character)
        for t in range(1, self.max_t+1):
            for p in range(1, self.max_p+1):
                logger.debug('Evaluating t={} p={}'.format(t, p))

                # If p is a '.', then we're guaranteed to be ok. In that case, it just matters
                # whether our solution for one smaller t and one smaller p worked, and we set
                # this result to equal that one
                if self.pchar_at_M_idx(p) == '.':
                    self.M[t][p] = self.M[t-1][p-1]
                    logger.debug(LOG_STATE_MSG.format(t, p, "p == '.'"))
                    logger.debug(LOG_RESULT_MSG.format(t, p, self.M[t-1][p-1]))

                elif self.pchar_at_M_idx(p) == "*":
                    logger.debug(LOG_STATE_MSG.format(t, p, "p == '*'"))
                    # We could try matching 0 characters for '<prev_char>*', i.e. 'a*' = ''
                    two_fewer_p_worked_same_t = self.M[t][p-2]
                    # We could try matching 1 instance of the last character, i.e. 'a*' = 'a'
                    one_fewer_p_worked_same_t = self.M[t][p-1]

                    prev_p_was_dot = (self.pchar_at_M_idx(p-1) == ".")
                    prev_p_matches_this_t = (self.pchar_at_M_idx(p-1) == self.tchar_at_M_idx(t))
                    prev_p_was_dot_or_matched_this_t = prev_p_was_dot or prev_p_matches_this_t

                    same_pattern_one_fewer_t_was_success = self.M[t-1][p]

                    if two_fewer_p_worked_same_t \
                       or one_fewer_p_worked_same_t \
                       or (prev_p_was_dot_or_matched_this_t and same_pattern_one_fewer_t_was_success):
                        self.M[t][p] = True
                        logger.debug(LOG_RESULT_MSG.format(t, p, True))

                        for val in DEBUG_VARS:
                            logger.debug('    {}: {}'.format(val, eval(val)))

                # Last situation: self.pchar_at_M_idx(p) is a regular character (not a . or *)
                else:
                    logger.debug(LOG_STATE_MSG.format(t, p, "p != '*' and p != '.'"))
                    one_fewer_t_and_p_was_success = self.M[t-1][p-1]
                    this_p_matches_this_t = (self.pchar_at_M_idx(p) == self.tchar_at_M_idx(t))
                    self.M[t][p] = one_fewer_t_and_p_was_success and this_p_matches_this_t
                    logger.debug(LOG_RESULT_MSG.format(t, p, one_fewer_t_and_p_was_success and this_p_matches_this_t))

                # Adding blank line to debugging output to separate each (t, p) combination
                logger.debug('')

        return self.M[self.max_t][self.max_p]
