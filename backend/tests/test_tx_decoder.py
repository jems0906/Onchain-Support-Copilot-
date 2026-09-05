from app.onchain import decode_revert_data


def test_decoder_handles_panic_selector():
    assert decode_revert_data("0x4e487b71" + "0" * 64) == "Contract panicked during execution"
