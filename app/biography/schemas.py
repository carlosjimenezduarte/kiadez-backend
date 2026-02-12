from datetime import date

from pydantic import BaseModel, Field, model_validator


class BiographyPersonalInfoUpdateRequest(BaseModel):
    birth_name: str | None = Field(default=None, max_length=200)
    birth_date: date | None = None
    birth_city: str | None = Field(default=None, max_length=120)
    birth_region: str | None = Field(default=None, max_length=120)
    birth_country: str | None = Field(default=None, max_length=120)
    residence: str | None = Field(default=None, max_length=255)
    nationality: str | None = Field(default=None, max_length=120)
    native_language: str | None = Field(default=None, max_length=120)
    pseudonyms: str | None = Field(default=None, max_length=300)

    @model_validator(mode="after")
    def normalize_text_fields(self):
        text_fields = (
            "birth_name",
            "birth_city",
            "birth_region",
            "birth_country",
            "residence",
            "nationality",
            "native_language",
            "pseudonyms",
        )
        for field_name in text_fields:
            value = getattr(self, field_name)
            if value is None:
                continue
            cleaned = value.strip()
            setattr(self, field_name, cleaned if cleaned else None)
        return self


class BiographyPersonalInfoOut(BaseModel):
    birth_name: str | None = None
    birth_date: date | None = None
    birth_city: str | None = None
    birth_region: str | None = None
    birth_country: str | None = None
    birth_display: str | None = None
    residence: str | None = None
    nationality: str | None = None
    native_language: str | None = None
    pseudonyms: str | None = None


class BiographyPhysicalTraitsUpdateRequest(BaseModel):
    height: str | None = Field(default=None, max_length=40)
    weight: str | None = Field(default=None, max_length=40)
    eyes: str | None = Field(default=None, max_length=80)
    hair: str | None = Field(default=None, max_length=80)

    @model_validator(mode="after")
    def normalize_text_fields(self):
        text_fields = ("height", "weight", "eyes", "hair")
        for field_name in text_fields:
            value = getattr(self, field_name)
            if value is None:
                continue
            cleaned = value.strip()
            setattr(self, field_name, cleaned if cleaned else None)
        return self


class BiographyPhysicalTraitsOut(BaseModel):
    height: str | None = None
    weight: str | None = None
    eyes: str | None = None
    hair: str | None = None


class BiographyEducationUpdateRequest(BaseModel):
    slot1: str | None = Field(default=None, max_length=255)
    slot2: str | None = Field(default=None, max_length=255)
    slot3: str | None = Field(default=None, max_length=255)
    slot4: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def normalize_text_fields(self):
        text_fields = ("slot1", "slot2", "slot3", "slot4")
        for field_name in text_fields:
            value = getattr(self, field_name)
            if value is None:
                continue
            cleaned = value.strip()
            setattr(self, field_name, cleaned if cleaned else None)
        return self


class BiographyEducationOut(BaseModel):
    slot1: str | None = None
    slot2: str | None = None
    slot3: str | None = None
    slot4: str | None = None


class BiographyCuriositiesUpdateRequest(BaseModel):
    favorite_superhero: str | None = Field(default=None, max_length=120)
    favorite_song: str | None = Field(default=None, max_length=255)
    favorite_food: str | None = Field(default=None, max_length=160)
    videogames: str | None = Field(default=None, max_length=500)
    favorite_book: str | None = Field(default=None, max_length=255)
    other_hobbies: str | None = Field(default=None, max_length=500)
    motto: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def normalize_text_fields(self):
        text_fields = (
            "favorite_superhero",
            "favorite_song",
            "favorite_food",
            "videogames",
            "favorite_book",
            "other_hobbies",
            "motto",
        )
        for field_name in text_fields:
            value = getattr(self, field_name)
            if value is None:
                continue
            cleaned = value.strip()
            setattr(self, field_name, cleaned if cleaned else None)
        return self


class BiographyCuriositiesOut(BaseModel):
    favorite_superhero: str | None = None
    favorite_song: str | None = None
    favorite_food: str | None = None
    videogames: str | None = None
    favorite_book: str | None = None
    other_hobbies: str | None = None
    motto: str | None = None


class BiographyProfessionalInfoUpdateRequest(BaseModel):
    occupation: str | None = Field(default=None, max_length=500)
    active_years: str | None = Field(default=None, max_length=120)

    @model_validator(mode="after")
    def normalize_text_fields(self):
        text_fields = ("occupation", "active_years")
        for field_name in text_fields:
            value = getattr(self, field_name)
            if value is None:
                continue
            cleaned = value.strip()
            setattr(self, field_name, cleaned if cleaned else None)
        return self


class BiographyProfessionalInfoOut(BaseModel):
    occupation: str | None = None
    active_years: str | None = None


class BiographyAboutUpdateRequest(BaseModel):
    display_name: str | None = Field(default=None, max_length=200)
    about_text: str | None = None

    @model_validator(mode="after")
    def normalize_text_fields(self):
        if self.display_name is not None:
            cleaned_name = self.display_name.strip()
            self.display_name = cleaned_name if cleaned_name else None
        if self.about_text is not None:
            cleaned_text = self.about_text.strip()
            self.about_text = cleaned_text if cleaned_text else None
        return self


class BiographyAboutOut(BaseModel):
    display_name: str | None = None
    about_text: str | None = None
    word_count: int = 0


class BiographyDreamUpdateRequest(BaseModel):
    dream_title: str | None = Field(default=None, max_length=200)
    dream_text: str | None = None

    @model_validator(mode="after")
    def normalize_text_fields(self):
        if self.dream_title is not None:
            cleaned_title = self.dream_title.strip()
            self.dream_title = cleaned_title if cleaned_title else None
        if self.dream_text is not None:
            cleaned_text = self.dream_text.strip()
            self.dream_text = cleaned_text if cleaned_text else None
        return self


class BiographyDreamOut(BaseModel):
    dream_title: str | None = None
    dream_text: str | None = None
    word_count: int = 0


class BiographyProfessionalAchievementsUpdateRequest(BaseModel):
    section_title: str | None = Field(default=None, max_length=200)
    section_text: str | None = None

    @model_validator(mode="after")
    def normalize_text_fields(self):
        if self.section_title is not None:
            cleaned_title = self.section_title.strip()
            self.section_title = cleaned_title if cleaned_title else None
        if self.section_text is not None:
            cleaned_text = self.section_text.strip()
            self.section_text = cleaned_text if cleaned_text else None
        return self


class BiographyProfessionalAchievementsOut(BaseModel):
    section_title: str | None = None
    section_text: str | None = None
    word_count: int = 0


class BiographyLifeAchievementsUpdateRequest(BaseModel):
    section_title: str | None = Field(default=None, max_length=200)
    section_text: str | None = None

    @model_validator(mode="after")
    def normalize_text_fields(self):
        if self.section_title is not None:
            cleaned_title = self.section_title.strip()
            self.section_title = cleaned_title if cleaned_title else None
        if self.section_text is not None:
            cleaned_text = self.section_text.strip()
            self.section_text = cleaned_text if cleaned_text else None
        return self


class BiographyLifeAchievementsOut(BaseModel):
    section_title: str | None = None
    section_text: str | None = None
    word_count: int = 0


class BiographyFavoriteQuotesUpdateRequest(BaseModel):
    section_title: str | None = Field(default=None, max_length=200)
    section_text: str | None = None

    @model_validator(mode="after")
    def normalize_text_fields(self):
        if self.section_title is not None:
            cleaned_title = self.section_title.strip()
            self.section_title = cleaned_title if cleaned_title else None
        if self.section_text is not None:
            cleaned_text = self.section_text.strip()
            self.section_text = cleaned_text if cleaned_text else None
        return self


class BiographyFavoriteQuotesOut(BaseModel):
    section_title: str | None = None
    section_text: str | None = None
    word_count: int = 0
