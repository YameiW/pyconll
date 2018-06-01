from pyconllu.unit import Token


def _test_token_members(token, id, form, lemma, upos, xpos, feats, head,
                        deprel, deps, misc):
    # NOTE: This uses equality for None comparison, is it worth doing differently?
    assert token.id == id
    assert token.form == form
    assert token.lemma == lemma
    assert token.upos == upos
    assert token.xpos == xpos
    assert token.feats == feats
    assert token.head == head
    assert token.deprel == deprel
    assert token.deps == deps
    assert token.misc == misc


def test_construction():
    """
    Test the normal construction of a general token.
    """
    token_line = '7	vie	vie	NOUN	_	Gender=Fem|Number=Sing	4	nmod	_	SpaceAfter=No\n'
    token = Token(token_line)

    _test_token_members(token, '7', 'vie', 'vie', 'NOUN', None, {
        'Gender': set(('Fem', )),
        'Number': set(('Sing', ))
    }, '4', 'nmod', {}, {'SpaceAfter': set(('No', ))})


def test_construction_no_newline():
    """
    Test the construction of a token with no newline at the end of the line.
    """
    token_line = '7	vie	vie	NOUN	_	Gender=Fem|Number=Sing	4	nmod	_	_'
    token = Token(token_line)

    _test_token_members(token, '7', 'vie', 'vie', 'NOUN', None, {
        'Gender': set(('Fem', )),
        'Number': set(('Sing', ))
    }, '4', 'nmod', {}, {})


def test_only_form_and_lemma():
    """
    Test construction when token line only has a form and lemma.
    """
    token_line = '10.1	micro-pays	micro-pays	_	_	_	_	_	_	_\n'
    token = Token(token_line)

    _test_token_members(token, '10.1', 'micro-pays', 'micro-pays', None, None,
                        {}, None, None, {}, {})


def test_multiple_features_modify():
    """
    Test modification of features.
    """
    token_line = '28	une	un	DET	_	' \
        'Definite=Ind|Gender=Fem|Number=Sing|PronType=Art	30	det	_	_\n'
    token = Token(token_line)

    _test_token_members(
        token, '28', 'une', 'un', 'DET', None, {
            'Definite': set(('Ind', )),
            'Gender': set(('Fem', )),
            'Number': set(('Sing', )),
            'PronType': set(('Art', ))
        }, '30', 'det', {}, {})

    # Somehow this word is definite and indefinite!
    token.feats['Definite'].add('Def')

    _test_token_members(
        token, '28', 'une', 'un', 'DET', None, {
            'Definite': set(('Ind', 'Def')),
            'Gender': set(('Fem', )),
            'Number': set(('Sing', )),
            'PronType': set(('Art', ))
        }, '30', 'det', {}, {})


def test_deps_construction():
    """
    Test construction of a token when the deps field is present.
    """
    token_line = '1	They	they	PRON	PRP	Case=Nom|Number=Plur	2	nsubj	2:nsubj|4:nsubj	_\n'
    token = Token(token_line)

    _test_token_members(token, '1', 'They', 'they', 'PRON', 'PRP', {
        'Case': set(('Nom', )),
        'Number': set(('Plur', ))
    }, '2', 'nsubj', {
        '2': 'nsubj',
        '4': 'nsubj'
    }, {})


def test_multiword_construction():
    """
    Test the creation of a token that is a multiword token line.
    """
    token_line = '8-9	du	_	_	_	_	_	_	_	_'
    token = Token(token_line)

    _test_token_members(token, '8-9', 'du', None, None, None, {}, None, None,
                        {}, {})
    assert token.is_multiword()


def test_to_string():
    """
    Test if a token's string representation is accurate.
    """
    token_line =  '26	surmonté	surmonter	VERB	_	' \
        'Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part	22	acl	_	_'
    token = Token(token_line)

    assert str(token) == token_line


def test_modify_unit_field_to_string():
    """
    Test a token's string representation after changing one of it's fields.
    """
    token_line = '33	cintre	cintre	NOUN	_	Gender=Masc|Number=Sing	' \
        '30	nmod	_	SpaceAfter=No'
    token = Token(token_line)

    token.form = 'pain'
    token.lemma = 'pain'

    new_token_line = '33	pain	pain	NOUN	_	' \
        'Gender=Masc|Number=Sing	30	nmod	_	SpaceAfter=No'

    assert str(token) == new_token_line


def test_modify_dict_field_to_string():
    """
    Test a token's string representation after adding a feature.
    """
    token_line = '33	cintre	cintre	NOUN	_	Gender=Masc|Number=Sing	' \
        '30	nmod	_	SpaceAfter=No'
    token = Token(token_line)

    token.feats['Gender'].add('Fem')

    new_token_line = '33	cintre	cintre	NOUN	_	' \
        'Gender=Fem,Masc|Number=Sing	30	nmod	_	SpaceAfter=No'

    assert str(token) == new_token_line


def test_remove_feature_to_string():
    """
    Test a token's string representation after removing a feature completely.
    """
    token_line = '33	cintre	cintre	NOUN	_	Gender=Masc|Number=Sing	' \
        '30	nmod	_	SpaceAfter=No'
    token = Token(token_line)

    del token.feats['Gender']

    new_token_line = '33	cintre	cintre	NOUN	_	' \
        'Number=Sing	30	nmod	_	SpaceAfter=No'

    assert str(token) == new_token_line


def test_underscore_construction():
    """
    Test construction of token without empty assumption and no form or lemma.
    """
    token_line = '33	_	_	PUN	_	_	30	nmod	_	SpaceAfter=No'
    token = Token(token_line, empty=False)

    _test_token_members(token, '33', '_', '_', 'PUN', None, {}, '30', 'nmod',
                        {}, {'SpaceAfter': set(('No', ))})


def test_empty_form_present_lemma():
    """
    Test construction of token without empty assumption and no form but a present lemma.
    """
    token_line = '33	hate	_	VERB	_	_	30	nmod	_	SpaceAfter=No'
    token = Token(token_line, empty=False)

    _test_token_members(token, '33', 'hate', None, 'VERB', None, {}, '30',
                        'nmod', {}, {'SpaceAfter': set(('No', ))})


def test_empty_lemma_present_form():
    """
    Test construction of token without empty assumption and no lemma but a present form.
    """
    token_line = '33	_	hate	VERB	_	_	30	nmod	_	SpaceAfter=No'
    token = Token(token_line, empty=False)

    _test_token_members(token, '33', None, 'hate', 'VERB', None, {}, '30',
                        'nmod', {}, {'SpaceAfter': set(('No', ))})