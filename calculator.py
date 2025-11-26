def calculate_from_gross(gross: float, vat_rate: float):
    """
    Compute net amount and VAT from a gross amount.
    vat_rate can be provided as a percent (e.g. 20) or decimal (e.g. 0.2).
    Returns (net, vat).
    """
    if vat_rate > 1:
        rate = vat_rate / 100.0
    else:
        rate = vat_rate
    if rate < 0 or gross < 0:
        raise ValueError("Gross and VAT rate must be non-negative")
    net = gross / (1 + rate) if (1 + rate) != 0 else gross
    vat = gross - net
    return net, vat

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Calculate VAT and net amount from gross amount")
    parser.add_argument("-g", "--gross", type=float, help="Gross amount (including VAT)")
    parser.add_argument("-r", "--rate", type=float, default=20.0,
                        help="VAT rate as percent (e.g. 20) or decimal (e.g. 0.2). Default 20")
    args = parser.parse_args()

    if args.gross is None:
        try:
            args.gross = float(input("Enter gross amount: ").strip())
        except Exception:
            print("Invalid gross amount"); return

    try:
        net, vat = calculate_from_gross(args.gross, args.rate)
    except ValueError as e:
        print("Error:", e); return

    display_rate = args.rate / 100.0 if args.rate > 1 else args.rate
    print(f"Gross: {args.gross:,.2f}")
    print(f"Net:   {net:,.2f}")
    print(f"VAT:   {vat:,.2f}")
    print(f"VAT rate: {display_rate:.2%}")

if __name__ == "__main__":
    main()