class BaseValidation:
    def validate(self, validation_code: str | tuple[str, ...], checking: str) -> bool:
        print(f"BaseValidation.validate {validation_code=}")
        print(f"BaseValidation.validate {checking=}")
        return True


class ValidationPB(BaseValidation):
    def validate(
        self, validation_code=("PB", "QV", "PV"), checking: str = "Fatal"
    ) -> bool:
        print(f"Validation.validate {validation_code=}")
        print(f"Validation.validate {checking=}")


class ValidationQV(ValidationPB):
    def validate(self, validation_code, checking) -> bool:
        print(f"Validation.validate {validation_code=}")
        print(f"Validation.validate {checking=}")


validation = ValidationQV()
validation.validate("PB", "Warning")
