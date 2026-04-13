class CategoryError(Exception):
    pass

class CategoryValidationError(CategoryError):
    pass

class CategoryNotFoundError(CategoryError):
    pass

class CategoryNameExistsError(CategoryError):
    pass

class CategorySlugExistsError(CategoryError):
    pass

class CategoryParentNotFoundError(CategoryError):
    pass

class CategoryCircularReferenceError(CategoryError):
    pass

class CategoryHasChildrenError(CategoryError):
    pass