from rapidfuzz import fuzz

class SearchFuzzService:

    @staticmethod
    def fuzzy_filter(queryset, search, threshold=70):
        return [
            q for q in queryset
            if fuzz.partial_ratio(search.lower(), q.title.lower()) >= threshold
        ]