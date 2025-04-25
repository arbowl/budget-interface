"""Cards module for credit card rewards and categories."""

MARRIOTT_CPP_MODIFIER = 0.7


class Rewards:
    """Reward structure for a card"""

    _default_rates: dict[str, float] = {
        "other": 1.0,
        "rotating": 1.0,
        "dining": 1.0,
        "groceries": 1.0,
        "gas": 1.0,
        "entertainment": 1.0,
        "flights": 1.0,
        "hotels": 1.0,
        "rentals": 1.0,
    }

    def __init__(self, **rates: float) -> None:
        merged = {**self._default_rates, **rates}
        for category, rate in merged.items():
            setattr(self, category, rate)

    def __repr__(self) -> str:
        return f"Rewards({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

    def __getitem__(self, item: str) -> float:
        """Get the reward multiplier for a category"""
        return getattr(self, item.lower(), 1.0)


cards: dict[str, Rewards] = {
    "Venture X": Rewards(
        other=2.0,
        rotating=2.0,
        dining=2.0,
        groceries=2.0,
        gas=2.0,
        entertainment=2.0,
        flights=5.0,
        hotels=10.0,
        rentals=10.0,
    ),
    "Discover It": Rewards(rotating=5.0),
    "Savor": Rewards(
        dining=3.0,
        groceries=3.0,
        entertainment=3.0,
    ),
    "Ritz-Carlton": Rewards(
        other=2 * MARRIOTT_CPP_MODIFIER,
        rotating=2 * MARRIOTT_CPP_MODIFIER,
        dining=3 * MARRIOTT_CPP_MODIFIER,
        groceries=3 * MARRIOTT_CPP_MODIFIER,
        gas=3 * MARRIOTT_CPP_MODIFIER,
        entertainment=2 * MARRIOTT_CPP_MODIFIER,
        flights=2 * MARRIOTT_CPP_MODIFIER,
        hotels=6 * MARRIOTT_CPP_MODIFIER,
        rentals=2 * MARRIOTT_CPP_MODIFIER,
    ),
    "Cash": Rewards(
        other=0.0,
        rotating=0.0,
        dining=0.0,
        groceries=0.0,
        gas=0.0,
        entertainment=0.0,
        flights=0.0,
        hotels=0.0,
        rentals=0.0,
    ),
}
