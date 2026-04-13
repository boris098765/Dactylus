class LexemeError(Exception):
    pass

class LexemeValidationError(LexemeError):
    pass

class LexemeNotFoundError(LexemeError):
    pass

class LexemeTextExistsError(LexemeError):
    pass

class LexemeSlugExistsError(LexemeError):
    pass

class LexemeHasComposesError(LexemeError):
    pass