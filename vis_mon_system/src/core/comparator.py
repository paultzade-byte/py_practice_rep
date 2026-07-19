#src/core/comparator.py

import hashlib
from dataclasses import dataclass
from PIL import Image
import imagehash
import io

from imagehash import ImageHash

DEFAULT_DRIFT_THRESHOLD = 5

@dataclass
class ComparisonResult:
    md5_changed: bool
    visual_hamming_distance: int
    drift_detected: bool

class ImageComparator:
    def __init__(self, drift_threshold: int = DEFAULT_DRIFT_THRESHOLD):
        self.drift_threshold =  drift_threshold

    @staticmethod
    def _md5(data: bytes) -> str:
        return hashlib.md5(data).hexdigest()

    @staticmethod
    def _phash(data: bytes) -> ImageHash:
        return imagehash.phash(Image.open(io.BytesIO(data)))

    def compare(self, current_bytes: bytes, previous_bytes: bytes) -> ComparisonResult:
        md5_changed = self._md5(current_bytes) != self._md5(previous_bytes)
        # imagehash/numpy returns numpy.int64 and numpy.bool_
        # cast to regular Python types so that `is True`/`is False` and serialization
        # (e.g. to a database or JSON) are performed predictably.
        distance = int(self._phash(current_bytes) - self._phash(previous_bytes))

        return ComparisonResult(
            md5_changed=md5_changed,
            visual_hamming_distance=distance,
            drift_detected=bool(distance > self.drift_threshold),
        )