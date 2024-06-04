from typing import Literal as Literal

"""
Obtain SID, AUTH_TOKEN, PHONE from Twilio and RECEIVER is registered number for free-tier account
"""

class Configuration:
    SID: str
    AUTH_TOKEN: str
    PHONE: str
    RECEIVER: str

    def change(variable: Literal["SID", "AUTH_TOKEN", "PHONE", "RECEIVER"], value: str):
        """Change value of CONSTANT

        Args:
            variable (Literal[&#39;SID&#39;, &#39;AUTH_TOKEN&#39;, &#39;PHONE&#39;, &#39;RECEIVER&#39;]): Name of constant to update
            value (str): Value for constant to update with
        """
        var_l = list(
            filter(
                lambda x: not x.startswith("__") and x.isupper(),
                list(vars(Configuration).keys()),
            )
        )

        if variable in var_l:
            setattr(Configuration, variable, value)
