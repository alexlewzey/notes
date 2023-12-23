"""Convert seconds into human-readable string."""


def hr_seconds(seconds: float) -> str:
    if seconds == 0:
        return "now"
    seconds_in_duration = [
        ["year", 31536000],
        ["day", 86400],
        ["hour", 3600],
        ["minute", 60],
        ["second", 1],
    ]
    num_units = []
    for idx, (unit, seconds_per_unit) in enumerate(seconds_in_duration):
        num_unit, seconds = divmod(seconds, seconds_per_unit)
        if num_unit > 0:
            unit = unit if num_unit == 1 else unit + "s"
            num_units.append(f"{num_unit} {unit}")
    output = (
        num_units[0]
        if len(num_units) == 1
        else ", ".join(num_units[:-1]) + f" and {num_units[-1]}"
    )
    return output


for i in [1241234, 60, 400, 181, 0]:
    print(hr_seconds(i))
