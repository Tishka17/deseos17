from dataclasses import dataclass


@dataclass
class Pagination:
    limit: int
    offset: int
